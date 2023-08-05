import sys
import os
import time
import pytz
import base64
import boto3
import botocore
import logging
import subprocess
import traceback
import json
import yaml
import shutil
import threading
from datetime import datetime
from github import Github
from botocore.exceptions import WaiterError

logging.basicConfig(level=logging.INFO)


# exception hook so errors raise to main thread
def exception_hook(args):
    traceback.print_exc()
    globals()['_call_on_all_errors'] = True


# set the exception hook
threading.excepthook = exception_hook


class EC2Manager:
    def __init__(self, **kwargs):
        # needed envs
        self._repo = os.environ.get('REPO', kwargs.get('repo'))
        self._github_user = os.environ.get('GITHUB_USERNAME', kwargs.get('github_username'))
        self._github_token = os.environ.get('GITHUB_TOKEN', kwargs.get('github_token'))

        # optional envs
        self._config_file = os.environ.get('EC2_MANAGER_CONFIG', kwargs.get('config') or 'config.yaml')
        self._commit = os.environ.get('COMMIT', 'master')
        self._terraform_directory = os.environ.get(
            'TERRAFORM_DIRECTORY', os.path.join(os.getcwd(), 'terraform')
        )
        self._template_directory = os.path.join(os.path.dirname(__file__), 'template')
        self._repo_url = (
            f'https://{self._github_user}:{self._github_token}@github.com/{self._github_user}/{self._repo}.git'
        )
        self._max_attempts = int(os.environ.get('MAX_TIMEOUT', 600))

        self._github_client = Github(self._github_token)

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(level=logging.INFO)

        # only when initialize with a config
        if self._config_file:
            # internal variables
            self._config = self._get_config()
            self._aws_default_region = self._config.get('aws_region')
            self._type = self._config.get('type')
            self._vpc_name = self._config.get('vpc_name')
            self._public_subnet_cidr = self._config.get('public_subnet_cidr')
            self._expose_docker_daemons = int(self._config.get('expose_docker_daemons', 0))
            self._private_subnet_cidr = self._config.get('private_subnet_cidr', '')
            self._instance_names = self._get_instance_names()
            self._instance_repo_updates = self._get_instance_repo_updates()

            # boost the pool size of urllib to handle as many concurrent connection as there are instances
            client_config = botocore.config.Config(
                max_pool_connections=len(self._instance_names),
            )
            self._aws_session = boto3.Session(region_name=self._aws_default_region)
            self._ssm_client = self._aws_session.client('ssm', config=client_config)
            self._ec2_client = self._aws_session.client('ec2', config=client_config)
            self._s3_client = self._aws_session.client('s3', config=client_config)

            self._github_client = Github(
                login_or_token=self._github_token,
                pool_size=len(self._instance_names)
            )

            account_number = self._aws_session.client('sts').get_caller_identity().get('Account')
            if not account_number:
                raise ValueError(
                    'Please set the name of your terraform backend bucket with the AWS_BACKEND_BUCKET '
                    'environment variable.'
                )
            self._aws_backend_bucket = os.environ.get('AWS_BACKEND_BUCKET', f'{account_number}-terraform-state')
            self._aws_backend_key = f'{self._type}.tfstate'

    def _get_config(self):
        """
        Gets the config data.

        :returns: A dictionary of file data.
        :rtype: dict
        """
        if os.path.exists(self._config_file):
            with open(self._config_file, 'r') as config_file:
                return yaml.safe_load(config_file)
        return {}

    @staticmethod
    def _get_encoded_envs(encoded_string):
        """
        Gets environment variables from the given encoded string.

        :param str encoded_string: A env file encoded as a base64 string.
        :returns: A dictionary of environment variables.
        :rtype: dict
        """
        # decode the env file
        env_file_contents = base64.b64decode(encoded_string).decode('utf-8')
        return {line.split('=')[0]: line.split('=')[1].strip("'").strip('"') for line in env_file_contents.split('\n')
                if '=' in line}

    @staticmethod
    def encode_string(string):
        """
        Encodes string to base64 string
        """
        return str(base64.b64encode(string.encode('utf-8'))).strip("b'").strip("'")

    def _get_working_directory(self, working_directory):
        """
        Gets the working directory relative to the repo

        :returns: Working directory path.
        :rtype: str
        """
        path = os.path.normpath(os.path.join(self._repo, working_directory)).replace(os.path.sep, '/')
        return f'./{path}'

    def _get_instance_id(self, name, try_once=False, attempts=0):
        """
        Get the instance id by tag name:

        :param str name: The name of the instance.
        :param bool name: Whether to make one attempt to get the instance id.
        :param int attempts: The number of attempts made to get the instance id.
        :returns: Instance id.
        :rtype: str
        """
        if not try_once:
            self._logger.info(f"{name} has been trying to get its instance id for {attempts} secs...")
        instance_id = self.list_instances().get(name, {}).get('instance_id')
        if not instance_id and attempts < self._max_attempts and not try_once:
            time.sleep(5)
            instance_id = self._get_instance_id(name, try_once, attempts + 5)
        return instance_id

    def _get_instance_names(self):
        """
        Gets a list of instance names whose instances should be created.

        :return list[str]: A list of instance names.
        """
        instances = self._config.get('instances') or {}
        return list(instances.keys())

    def _get_instance_repo_updates(self):
        """
        Gets a list of instance names whose repos should be updated.

        :return list[str]: A list of instance names.
        """
        instances = self._config.get('instances') or {}
        return [key for key, value in instances.items() if value.get('update')]

    def _get_commit_time(self):
        """
        Gets the time of the commit.

        :return datetime: A UTC datetime object.
        """
        if self._commit not in ['master', 'main']:
            repo = self.get_repo()
            commit_time = repo.get_commit(self._commit).last_modified
            return datetime.strptime(commit_time, '%a, %d %b %Y %H:%M:%S %Z').astimezone(pytz.UTC)

    def _get_instance_data(self):
        """
        Gets all the instance's environment variables.

        :return dict: A dictionary of instance names and their environment variables.
        """
        instances = self._config['instances']
        default_ports = [{'from_port': 2375, 'to_port': 2375, 'protocol': 'tcp'}] if self._expose_docker_daemons else []

        return {name: {
            'commands': {
                'start': instances[name].get('commands', {}).get('start', 'docker-compose up --detach'),
                'stop': instances[name].get('commands', {}).get('stop', 'docker-compose down'),
                'logs': instances[name].get('commands', {}).get('logs', 'docker-compose logs')
            },
            'volume_size': instances[name].get('volume_size', 8),
            'instance_type': instances[name].get('instance_type', 't4g.nano'),
            'working_directory': instances[name].get('working_directory', 'compose'),
            'ports': instances[name].get('ports', []) + default_ports,
            'envs': {
                'NAME': name,
                'REPO': self._repo,
                'COMMIT': self._commit,
                **instances[name].get('envs', {}),
                **self._get_encoded_envs(os.environ.get(instances[name].get('encoded_env_file_variable', ''), ''))
            }
        } for name in self._instance_repo_updates}

    def _status_check(self, name, status):
        """
        Check for the given status on the ec2 instance by id.

        :param str name: The name of the instance.
        :param str status: The name of the ec2 instance status check to wait for.
        """
        instance_id = self._get_instance_id(name)
        self._logger.info(f"{name} instance {instance_id} is checking if its status is {status.split('_')[-1]}")
        if instance_id:
            try:
                waiter = self._ec2_client.get_waiter(status)
                waiter.wait(InstanceIds=[instance_id])
                self._logger.info(f"{name} instance {instance_id} is {status.split('_')[-1]}")
            except WaiterError:
                logging.error(f"{name} status check of instance {instance_id} failed")
        else:
            self._logger.info(f"{name} instance does not exist")

    def _create_backend_bucket(self):
        """
        Creates terraform backend bucket if it doesn't exist.
        """
        buckets = [item['Name'] for item in self._s3_client.list_buckets().get('Buckets', [])]
        if self._aws_backend_bucket not in buckets:
            self._logger.info(f'Creating Terraform backend...')
            self._s3_client.create_bucket(
                ACL='private',
                Bucket=self._aws_backend_bucket
            )
            waiter = self._s3_client.get_waiter('bucket_exists')
            waiter.wait(Bucket=self._aws_backend_bucket)

    def _init_terraform(self):
        """
        Runs terraform init.
        """
        self._create_backend_bucket()
        self._logger.info(f'Initializing Terraform backend...')
        process = subprocess.run([
            'terraform',
            'init',
            f'-backend-config=key={self._aws_backend_key}',
            f'-backend-config=bucket={self._aws_backend_bucket}'
        ],
            env=os.environ,
            cwd=self._terraform_directory
        )
        if process.returncode != 0:
            raise RuntimeError('Failed to initialize terraform')

    def _apply_terraform(self):
        """
        Runs terraform apply that creates the ec2 instances.
        """
        outputs = self.get_terraform_outputs()
        if outputs.get('instances', {}).get('value') != self._instance_names:
            self._logger.info(f'Terraform instances...')
            instances = self.encode_string(json.dumps(self._get_instance_data()))

            process = subprocess.run(
                [
                    'terraform',
                    'apply',
                    '-auto-approve',
                    '-var',
                    f'type={self._type}',
                    '-var',
                    f'vpc_name={self._vpc_name}',
                    '-var',
                    f'public_subnet_cidr={self._public_subnet_cidr}',
                    '-var',
                    f'private_subnet_cidr={self._private_subnet_cidr}',
                    '-var',
                    f'aws_region={self._aws_default_region}',
                    '-var',
                    f'expose_docker_daemons={self._expose_docker_daemons}',
                    '-var',
                    f'instances={instances}'
                ],
                env=os.environ,
                cwd=self._terraform_directory
            )
            if process.returncode != 0:
                raise RuntimeError('Failed to apply terraform')

    def _destroy_terraform(self):
        """
        Runs terraform destroy.
        """
        self._logger.info(f'Destroying resources...')
        instances = self.encode_string(json.dumps(self._get_instance_data()))

        process = subprocess.run(
            [
                'terraform',
                'destroy',
                '-auto-approve',
                '-var',
                f'type={self._type}',
                '-var',
                f'vpc_name={self._vpc_name}',
                '-var',
                f'public_subnet_cidr={self._public_subnet_cidr}',
                '-var',
                f'private_subnet_cidr={self._private_subnet_cidr}',
                '-var',
                f'aws_region={self._aws_default_region}',
                '-var',
                f'expose_docker_daemons={self._expose_docker_daemons}',
                '-var',
                f'instances={instances}'
            ],
            env=os.environ,
            cwd=self._terraform_directory
        )
        if process.returncode != 0:
            raise RuntimeError('Failed to run terraform destroy')

    def _call_on_all(self, callable_instance, items, extra_args=None, **kwargs):
        """
        Helper method for calling a given method on all provided.

        :param callable callable_instance: A callable.
        :param Any items: A list of items to call.
        :param list extra_args: A list of extra arguments.
        :param bool join: Whether or not to join the threads.
        :return list[Thread]: A list of threads.
        """
        globals()['_call_on_all_errors'] = False

        if not extra_args:
            extra_args = []

        if type(items) != dict:
            if type(items) != list:
                items = list(items)
            new_items = {item: {} for item in items}
        else:
            new_items = items

        threads = []
        # begin call on each item in a separate thread
        for name, data in new_items.items():
            args = []
            args.insert(0, name)
            if data:
                args.insert(1, data)

            thread = threading.Thread(
                name=name,
                target=callable_instance,
                args=args + extra_args,
                kwargs=kwargs
            )
            thread.start()
            threads.append(thread)

        # join all threads which waits for each call to finish
        if kwargs.get('join', True):
            for thread in threads:
                thread.join()
            return []

        # stop the main process if a thread created an error
        if globals()['_call_on_all_errors']:
            sys.exit(1)

        return threads

    def _await_instances(self):
        """
        Waits till all ec2 instances have a status of ok.
        """
        self._call_on_all(
            callable_instance=self._status_check,
            items=self._get_instance_names(),
            extra_args=['instance_status_ok']
        )

    def get_terraform_outputs(self):
        """
        Gets the output from terraform state.

        :returns: Terraform outputs.
        :rtype: dict
        """
        self._logger.info(f'Exporting Terraform outputs...')
        try:
            return json.loads(subprocess.check_output(
                ['terraform', 'output', '-json'],
                env=os.environ,
                cwd=self._terraform_directory
            ))
        except:
            return {}

    def get_repo(self):
        """
        Gets the repo instance.
        """
        return self._github_client.get_repo(full_name_or_id=f'{self._github_user}/{self._repo}')

    def get_docker_logs(self, name, data):
        """
        Gets the log output from the docker container.
        """
        self._logger.info(f'{name} getting logs...')
        working_directory = self._get_working_directory(data['working_directory'])
        self.run_command(name, [
            f'cd {working_directory} ',
            data['commands']['logs']
        ])

    def list_instances(self):
        """
        List all ec2 instances.

        :return dict: A dictionary of data for all instances in the region.
        """
        instances = {}
        response = self._ec2_client.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if instance['State']['Name'] == 'running':
                    tags = instance.get('Tags', [])
                    for tag in tags:
                        if tag['Key'] == 'Name':
                            instances[tag['Value']] = {
                                'instance_id': instance.get('InstanceId'),
                                'private_ip_address': instance.get('PrivateIpAddress'),
                                'public_ip_address': instance.get('PublicIpAddress'),
                            }
        return instances

    def run_command(self, name, commands, print_output=True):
        """
        Runs a command on the ec2 instance and waits for the response.

        :param str name: The name of the instance.
        :param list[str] commands: A list of commands.
        :param bool print_output: Whether or to print the stdout.
        :return str: The stdout.
        """
        instance_id = self._get_instance_id(name, try_once=True)
        if instance_id:
            error = False
            # run the command
            response = self._ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName='AWS-RunShellScript',
                Parameters={'commands': commands}
            )
            command_id = response['Command']['CommandId']

            # wait for the command to finish
            try:
                waiter = self._ssm_client.get_waiter('command_executed')
                waiter.wait(
                    CommandId=command_id,
                    InstanceId=instance_id,
                    WaiterConfig={
                        'Delay': 10,
                        'MaxAttempts': 120
                    }
                )
            except Exception as waiter_error:
                error = waiter_error

            # get the command response
            command_response = self._ssm_client.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id
            )

            # get the standard output and standard errors
            stdout = command_response.get('StandardOutputContent')
            stderr = command_response.get('StandardErrorContent')

            if error:
                raise RuntimeError(str(stdout) + str(stderr) + str(error))
            elif print_output:
                print(str(stdout) + str(stderr))

            return stdout
        else:
            raise RuntimeError(f'instance {instance_id} does not exist')

    def create_instances(self):
        """
        Creates the ec2 instances.
        """
        existing_instances = self.list_instances().keys()
        # if not all instances that need to be updated exist run terraform
        if not all(instance_name in existing_instances for instance_name in self._instance_repo_updates):
            self._init_terraform()
            self._apply_terraform()

        # wait for each instance status to be ok
        self._await_instances()

    def _set_env_file(self, name, data):
        """
        Writes a env file to disk in the working directory.

        :param str name: The name of the instance.
        :param dict data: The instance's data.
        """
        self._logger.info(f'{name} setting env file...')
        env_file_content = '\n'.join([f'{key}={value}' for key, value in data['envs'].items()])
        working_directory = self._get_working_directory(data['working_directory'])
        self.run_command(name, [
            f'cd {working_directory}',
            f'echo "{env_file_content}" > .env'
        ], print_output=False)

    def _update_repo(self, name):
        """
        Updates a single instance repo.
        """
        if self._repo not in self.run_command(name, ['ls'], print_output=False):
            self._logger.info(f'{name} cloning {self._repo}')
            self.run_command(name, [f'git clone {self._repo_url}'])

        self._logger.info(f'{name} checking out {self._commit}')
        self.run_command(name, [
            f'cd ./{self._repo}',
            'git fetch',
            'git pull',
            # f'git -c advice.detachedHead=false checkout {self._commit}'
        ])

    def _stop(self, name, data):
        """
        Stops a single docker container if it is already running.
        """
        # check if docker is already running
        result = list(filter(None, self.run_command(name, ['docker ps'], print_output=False).split('\n')))
        if len(result) > 1:
            # then compose down
            self._logger.info(f'{name} stopping...')
            working_directory = self._get_working_directory(data['working_directory'])
            self.run_command(name, [
                f'cd {working_directory} ',
                data['commands']['stop']
            ])

    def _start(self, name, data):
        """
        Runs start command on a single instance.
        """
        self._set_env_file(name, data)
        self._logger.info(f'{name} starting...')
        working_directory = self._get_working_directory(data['working_directory'])
        self.run_command(name, [
            f'cd {working_directory} ',
            data['commands']['start'],
        ])

    def update_repos(self):
        """
        Updates the code in the instance repos.
        """
        self._call_on_all(
            callable_instance=self._update_repo,
            items=self._instance_repo_updates,
        )

    def stop(self):
        """
        Runs stop if a docker container is already running.
        """
        self._call_on_all(
            callable_instance=self._stop,
            items=self._get_instance_data(),
        )

    def start(self):
        """
        Runs start command on the instances.
        """
        self._call_on_all(
            callable_instance=self._start,
            items=self._get_instance_data(),
        )

    def init(self):
        """
        Initializes the project
        """
        destination = os.path.join(os.getcwd())
        if not os.path.exists(self._terraform_directory):
            shutil.copytree(
                src=self._template_directory,
                dst=destination,
                dirs_exist_ok=True
            )
            self._logger.info(f'Initialized project at "{destination}"')
        else:
            self._logger.info(f'Project is already initialized project at "{destination}"')

    def apply(self):
        """
        Apply according to the config.
        """
        self.create_instances()
        self.update_repos()
        self.stop()
        self.start()

    def destroy(self):
        """
        Destroy resources created with the config.
        """
        self._init_terraform()
        self._destroy_terraform()

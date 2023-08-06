# Prerequisites

* Python 3.7
* AWS Credentials

# AWS Container Launcher (aws-container-launcher)

AWS Container Launcher makes it easy to programmatically run a Docker container in AWS using the Python package.

| WARNING: After processing a job, you are in charge of destroying the infrastructure. Do not forget to call the "destroy" method; otherwise, the instance will continue to operate and you will be charged by Amazon. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|


# Instance type determination

You can specify the instance type explicitly or set the CPU and memory, and the module will automatically select the optimal instance type for you.

# Examples

## Minimal example with providing an instance type

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 1'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 't3.micro',  # required. Alternatively, use 'cpu' and 'memory' parameters pair.
}

'''
Asynchronously running of an ECS task.
However, resource initializing happens synchronously (EC2, etc.) and takes up to 5 minutes
'''
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(10)

get_container_status_response = acl.get_container_status(entry_id)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

## Minimal example with providing 'cpu' and 'memory' pair

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 1'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'cpu': 1,  # required. Alternatively, use the 'instance_type' parameter for 'cpu' and 'memory' parameters pair.
    'memory': 4  # required. Alternatively, use the 'instance_type' parameter for 'cpu' and 'memory' parameters pair.
}

'''
Asynchronously running of an ECS task.
However, resource initializing happens synchronously (EC2, etc.) and takes up to 5 minutes
'''
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(10)

get_container_status_response = acl.get_container_status(entry_id)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

# Advanced

```
import time
import logging
import boto3
from botocore.config import Config
from aws_container_launcher import ContainerLauncher, RunStatus

logger = logging
logging.basicConfig(level=logging.INFO)

config = Config(
    retries={
        'max_attempts': 20,
        'mode': 'adaptive'
    }
)

amazon_ec2_best_instance_ec2_client = boto3.Session().client('ec2', config=config)


acl = ContainerLauncher({
    'monitoring_table_tags': {
        'k1': 'v1',
        'k2': 'v2'
    },  # optional. It is tagging for the monitoring DynamoDB table.
        # The DynamoDB table will be created if it doesn't exist and will be reused if it exists.
    'logger': logger,  # Optional
    'region': 'us-east-1',  # Optional. String.
    'spot_instance_deploying_timeout_in_minutes': 25,  # Optional. Integer. Default: 10.
                                                      # It is a timeout for waiting spot instance requesting
    'clients': {
        'amazon_ec2_best_instance_ec2_client': amazon_ec2_best_instance_ec2_client
        # Optional. The EC2 client, which used for the amazon-ec2-best-instance package
    }  # Optional                                       
})

entry_id = str(time.time()).replace('.', '')

start_container_input = {
    'commands': [
        'sleep 1'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'cpu': 1,  # required. Alternatively, use the 'instance_type' parameter for 'cpu' and 'memory' parameters pair.
    'memory': 4,  # required. Alternatively, use the 'instance_type' parameter for 'cpu' and 'memory' parameters pair.
    'id': entry_id,  # optional. The ID must be unique for each task.
                     # Otherwise, you will get the same status for an already completed job.
                     # If not provided, then ID will be generated automatically.
    'name_suffix': <name_suffix>,  # optional. The name_suffix must be unique for each job run.
    'ec2_sg_ids': [<security_group_id_1>, <security_group_id_2>],  # optional. Default: A default VPC security group
    'tags': {
        'k1': 'v1',
        'k2': 'v2'
    },  # optional
    'is_spot': True,  # Default: False
    'instance_type': 't3.micro',  # required. Alternatively, use 'cpu' and 'memory' parameters pair.
                                     # The instance type has priority over 'cpu' and 'memory' parameters pair.
    'storages': [
        {
            'type': 'fsx',
            'file_system_id': <file_system_id>,
            'dir': '/fsx'  # It is a path to access FSx space from an EC2 instance. Default: /fsx
        },
        {
            'type': 'ssd_instance_store'
        }
    ],  # optional
    'options': {
        'scaling_enabled': True
    },  # Used as a safety catch if you forgot to destroy the infrastructure after processing the job.
       # If the CPU activity for the EC2 instance is less than 1 percent for 3 hours,
       # the EC2 instance will be terminated by Auto Scaling Policy.
    'spot': {
        'max_interruption_frequency': 10
    },  # Optional. Integer (%). Default: 10. Max spot instance frequency interruption in percent.
       # Note: If you specify >=21, then the '>20%' rate is applied
       # It is used only if 'is_spot' == True
    'logs': {
        'ecs_task': {
            'group': '<cloud_watch_group>', 
            # Required. E.g., "/acl/ecs/task". Note: A group must exist
            'stream_prefix': f'acl-{random_id}'
            # Required
        }  # Optional. CloudWatch logs for an ECS task
    }  # Optional. CloudWatch logs   
}

'''
Asynchronously running of an ECS task.
However, resource initializing happens synchronously (EC2, etc.)
and takes up to 5 minutes
'''
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(10)

get_container_status_response = acl.get_container_status(entry_id)

status = get_container_status_response['status']

print(status)

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)


```

# Storage

## Amazon FSx for Lustre

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 120'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 'm5d.4xlarge',
    'storages': [
        {
            'type': 'fsx',
            'file_system_id': <file_system_id>,
            'dir': '/fsx'  # It is a path to access FSx space from an EC2 instance. Default: /fsx
        }
    ],
    'ecs_task_definition': {
        'volumes': [
            {
                'name': 'fsx_storage',
                'host': {
                    'sourcePath': '/fsx'  # Must be matched with "storages[.type == 'fsx'].dir"
                }
            }
        ],
        'containerDefinitions': {
            'mountPoints': [
                {
                    'sourceVolume': 'fsx_storage',
                    'containerPath': '/fsx',  # It is a path to access FSx space from a docker container.
                    'readOnly': False
                },
            ]
        },
    },
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(300)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

## SSD instance store

* It you specify instance type explicitly and instance type doesn't support NVMe SSD storage, then SSD instance store configuration is ignored
* If you specify CPU and memory pair then the package automatically pick up optimal instance type with instance store
* The solution automatically combines all ephemeral disks using RAID 0; thus, all disks are treated as one file system, and all space is available on the specified path

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 120'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 'm5d.4xlarge',  # required
    'storages': [
        {
            'type': 'ssd_instance_store',
            'dir': '/ssd1'  # It is a path to access SSD instance store space from an EC2 instance. Default: /ssd
        }
    ],
    'ecs_task_definition': {
        'volumes': [
            {
                'name': 'ssd_instance_store',
                'host': {
                    'sourcePath': '/ssd1'  # Must be matched with "storages[.type == 'ssd_instance_store'].dir"
                }
            }
        ],
        'containerDefinitions': {
            'mountPoints': [
                {
                    'sourceVolume': 'ssd_instance_store',
                    'containerPath': '/ssd',  # It is a path to access SSD instance store space from a docker container.
                    'readOnly': False
                }
            ]
        }
    }
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(300)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

## EFS

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 600'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 'm5d.4xlarge',  # required
    'ecs_task_definition': {
        'volumes': [
            {
                'name': 'efs',
                'efsVolumeConfiguration': {
                    'fileSystemId': <file_system_id>,
                    'rootDirectory': '/',
                    'transitEncryption': 'ENABLED',
                    'authorizationConfig': {
                        'accessPointId': <access_point_id>,
                        'iam': 'ENABLED'
                    }
                }
            }
        ],
        'containerDefinitions': {
            'mountPoints': [
                {
                    'sourceVolume': 'efs',
                    'containerPath': '/mnt/efs',
                    'readOnly': False
                }
            ],
            'workingDirectory': '/mnt/efs'
        }
    }
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(700)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

## EBS

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 300'
    ],
    'docker_image': 'ubuntu:latest',
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],
    'instance_type': 't3.micro',  # Alternatively, use 'cpu' and 'memory' parameters pair.
    'storages': [
        {
            'type': 'ebs',
            'device_name': '/dev/sdx',
            'volume_size': 100,
            'volume_type': 'gp2',  # Values: 'standard'|'io1'|'io2'|'gp2'|'sc1'|'st1'|'gp3'
            'dir': '/ebs1'  # Default: /ebs
        }
        #  Only one device with the "ebs" type is acceptable now at the same time.
    ],
    'ecs_task_definition': {
        'volumes': [
            {
                'name': 'ebs',
                'host': {
                    'sourcePath': '/ebs1'  # Must be matched with "storages[.type == 'ebs'].dir"
                }
            }
        ],
        'containerDefinitions': {
            'mountPoints': [
                {
                    'sourceVolume': 'ebs',
                    'containerPath': '/ebs1',  # It is a path to access EBS space from a docker container.
                    'readOnly': False
                }
            ]
        }
    }
}

'''
Asynchronously running of an ECS task.
However, resource initializing happens synchronously (EC2, etc.) and takes up to 5 minutes
'''
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(400)

get_container_status_response = acl.get_container_status(entry_id)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

# Privileged mode

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 600'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 't3.small',  # required
    'ecs_task_definition': {
        'containerDefinitions': {
            'privileged': True
        }
    }
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(700)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

# Spot instance

```
import time
import logging
from aws_container_launcher import ContainerLauncher, RunStatus

logger = logging
logging.basicConfig(level=logging.INFO)

acl = ContainerLauncher({
    'spot_instance_deploying_timeout_in_minutes': 25  # Optional. Integer. Default: 10.
                                                      # It is a timeout for waiting spot instance requesting
})

entry_id = str(time.time()).replace('.', '')

start_container_input = {
    'commands': [
        'sleep 1'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'cpu': 32,  # required. Alternatively, use the 'instance_type' parameter for 'cpu' and 'memory' parameters pair.
    'memory': 256,  # required. Alternatively, use the 'instance_type' parameter for 'cpu' and 'memory' parameters pair.
    'is_spot': True,  # Optional
    'spot': {
        'max_interruption_frequency': 15, # Optional. Integer (%). Default: 10. 
                                          # The maximum spot instance frequency interruption in percent.
                                          # Note: If you specify >=21, then the '>20%' rate is applied
                                          # It is used only if 'is_spot' == True
        'max_instance_type_candidates': 4,  # Optional. Integer. Default: 3. The maximum number of instance types participating as candidates for the request.
        'spot_allocation_strategy': 'capacity-optimized-prioritized'  # Optional. String. Default: 'capacity-optimized-prioritized'.
                                                                      # Possible values: lowest-price | capacity-optimized | capacity-optimized-prioritized.
                                                                      # Indicates how to allocate instances across Spot Instance pools.
    }  # Optional

}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

print(start_container_response)

entry_id = start_container_response['entry_id']

time.sleep(30)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

print(status)

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

# Scaling options

## Scaling in

Used as a safety catch if you forgot to destroy the infrastructure after processing the job.
Now CPUUtilization metric name is supported only.

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 1'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'cpu': 16,  # required. Alternatively, use the 'instance_type' parameter for 'cpu' and 'memory' parameters pair.
    'memory': 20,  # required. Alternatively, use the 'instance_type' parameter for 'cpu' and 'memory' parameters pair.
    'options': {
        'scaling_enabled': True,
        'scaling_options': {
            'period': 500,  # Optional. Integer. Default: 300.
                            # The length, in seconds. Valid values are 10, 30, and any multiple of 60.
            'evaluation_periods': 36,  # Optional. Integer. Default: 36.
                                       # The number of periods over which data is compared to the specified threshold.
            'threshold': 1.0  # Optional. Float. Default: 1.0.
                              # The value against which the specified statistic is compared.
        }
    }
}

start_container_response = acl.start_container(start_container_input)

print(start_container_response)

entry_id = start_container_response['entry_id']

time.sleep(30)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

print(status)

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

# IAM roles

## EC2 role

By default, an IAM role generated with arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role policy (default policy for the Amazon EC2 Role for Amazon EC2 Container Service).

If you need to add additional permissions, you need to add policy documents or managed policy ARNs:

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 600'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 't3.small',  # required
    'iam': {
        'ec2': {
            'policy_documents': [
                {
                    'Version': '2012-10-17',
                    'Statement': {
                        'Effect': 'Allow',
                        'Action': 'ec2:*',
                        'Resource': '*'
                    }
                },
                {
                    'Version': '2012-10-17',
                    'Statement': {
                        'Effect': 'Allow',
                        'Action': 's3:*',
                        'Resource': '*'
                    }
                }
            ],
            'managed_policy_arns': [
                'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
            ]
        }
    }  # optional
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(700)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

Alternatively, you can provide IAM Role ARN explicitly (ARN has priority):

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 600'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 't3.small',  # required
    'iam': {
        'ec2': {
            'arn': '<iam_role_arn>'
        }
    }  # optional
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(700)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

## ECS task role

By default, an IAM role is generated with no policies.

If you need to access any AWS resources from a container, you need to add policy documents:

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 600'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 't3.small',  # required
    'iam': {
        'ecs_task': {
            'policy_documents': [
                {
                    'Version': '2012-10-17',
                    'Statement': {
                        'Effect': 'Allow',
                        'Action': 'lambda:*',
                        'Resource': '*'
                    }
                },
                {
                    'Version': '2012-10-17',
                    'Statement': {
                        'Effect': 'Allow',
                        'Action': 'sns:*',
                        'Resource': '*'
                    }
                }
            ]
        }
    }  # optional
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(700)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

Alternatively, you can provide IAM Role ARN explicitly (ARN has priority):

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 600'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 't3.small',  # required
    'iam': {
        'ecs_task': {
            'arn': '<iam_role_arn>'
        }
    }  # optional
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(700)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```

## ECS task execution role

By default, an IAM role generated with arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy policy (provides access to other AWS service resources that are required to run Amazon ECS tasks).

Alternatively, you can provide IAM Role ARN explicitly (ARN has priority):

```
import time
from aws_container_launcher import ContainerLauncher, RunStatus

acl = ContainerLauncher()

start_container_input = {
    'commands': [
        'sleep 300'
    ],  # required
    'docker_image': 'ubuntu:latest',  # required
    'subnet_ids': [<subnet_id_1>, <subnet_id_2>],  # required
    'instance_type': 't3.small',  # required
    'iam': {
        'ecs_task_execution': {
            'arn': '<iam_role_arn>'
        }
    }
}

# Async running of an ECS task
start_container_response = acl.start_container(start_container_input)

entry_id = start_container_response['entry_id']

time.sleep(400)

get_container_status_response = acl.get_container_status(entry_id)

print(get_container_status_response)

status = get_container_status_response['status']

assert status == RunStatus.COMPLETED.name

acl.destroy(entry_id)

```
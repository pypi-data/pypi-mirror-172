# Prerequisites

* Python 3.7
* AWS Credentials

# AWS Container Launcher (aws-container-launcher)

AWS Container Launcher makes it easy to programmatically run a Docker container in AWS using the Python package.

| WARNING: After processing a job, you are in charge of destroying the infrastructure. Do not forget to call the "destroy" method; otherwise, the instance will continue to operate and you will be charged by Amazon. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|


# Instance type determination

You can specify the instance type explicitly or set the CPU and memory, and the package will automatically select the optimal instance type for you.

# Usage

To better understand, familiarize yourself with the available methods and the [start_container](doc/method/START_CONTAINER.MD) method in particular.

# Client

* [Client configuration](doc/method/START_CONTAINER.MD)

# Methods

* [start_container](doc/method/START_CONTAINER.MD)
* [get_container_status](doc/method/GET_CONTAINER_STATUS.MD)
* [get_container_record](doc/method/GET_CONTAINER_RECORD.MD)
* [destroy](doc/method/DESTROY.MD)
* [delete_monitoring_table](doc/method/DELETE_MONITORING_TABLE.MD)

# Storage

* [SSD instance store](doc/storage/SSD.MD)
* [EBS](doc/storage/EBS.MD)
* [Amazon FSx for Lustre](doc/storage/FSX.MD)
* [EFS](doc/storage/EFS.MD)

# Spot instance

* [Using spot instances](doc/SPOT_INSTANCE.MD)

# Scaling options

* [Scaling in](doc/scaling/SCALING_IN.MD)

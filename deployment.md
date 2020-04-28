
# Deployment

### Prerequisite

1. OS:
Ubuntu 18.04

1. Install docker
```bash
sudo apt update
sudo apt install docker.io
```
Or check the following guide.
https://docs.docker.com/install/linux/docker-ce/ubuntu/

### Get the docker images

All the docker images ready for use are uploaded to DockerHub.
https://hub.docker.com/repository/docker/ouankou/rds
The images contain all tools with proper configuration. Because Flask code could be updated frequently, they are not included in the docker image. Instead, they should be mounted into the docker container.

#### Metaservice
```bash
sudo docker pull racedetectionservice/rds:meta-local
```
#### ThreadSanitizer
```bash
sudo docker pull ouankou/rds:tsan-test
```
#### Archer
```bash
sudo docker pull ouankou/rds:archer-test
```
#### ROMP
```bash
sudo docker pull ouankou/rds:romp-test
```
#### Intel Inspector
A valid license is required to install and use Intel Inspector.
**We are not allowed to distribute it, so after pulling the base image, the user may need to install it in the corresponding container by yourself.**
We assume in the next steps, the user is able to set up a fully functional Intel Inspector.
```bash
sudo docker pull ouankou/rds:inspector
```

### Create a container

The tools have been configured in the docker image. Users need to set up the ports based on their actual environment.
In this case we assume the ports 5010, 5011, 5012, 5013 and 5014 are available for the usage of RDS.

#### Metaservice
```bash
sudo docker run -p 5010:5000 --name rds_meta ouankou/rds:meta-test &
```
#### Archer
```bash
sudo docker run -p 5011:5000 --name rds_archer ouankou/rds:archer-test &
```
#### ThreadSanitizer
```bash
sudo docker run -p 5013:5000 --name rds_tsan ouankou/rds:tsan-test &
```
#### ROMP
```bash
sudo docker run -p 5014:5000 --name rds_romp ouankou/rds:romp-test &
```
#### Intel Inspector
A valid license is required to install and use Intel Inspector.
**We are not allowed to distribute it, so after pulling the base image, the user may need to install it in the corresponding container by yourself.**
We assume in the next steps, the user is able to set up a fully functional Intel Inspector.
```bash
sudo docker run -p 5012:5000 --name rds_intel ouankou/rds:inspector
# enter the container and install the Intel Inspector with your own license
sudo docker exec -it rds_intel bash
...
```


### Start/Restart/Stop/Delete a container

```bash
sudo docker start rds_tsan
sudo docker restart rds_tsan
sudo docker stop rds_tsan
sudo docker rm rds_tsan
```

### Enter a container
After creating a container, run the following command to enter it for debugging or something else.
```bash
sudo docker exec -it rds_tsan bash
```

# Usage

### Send a request

Assume we have a file named `foo.c` to inspect.
```bash
curl -X POST -F "file=@foo.c" "localhost:5010/test?type=json"
```



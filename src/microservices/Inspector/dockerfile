
# Environment for the microservice Intel Inspector.
# Due to potential license issue, Intel Inspector is not installed via dockerfile, at lease for now.
# User can manually copy the installation file into a container and install manually.
# While doing so, user needs to enter the docker container as root temporarily instead of the default rds.

# Pull base image.
FROM ubuntu:18.04

# Add user
RUN groupadd -g 9999 rds && \
    useradd -r -u 9999 -g rds -m -d /home/rds rds

# Install packages.
RUN apt-get update && \
    apt-get install -y \
        apt-utils \
        bc \
        build-essential \
        cmake \
        cpio \
        curl \
        dialog \
        g++ \
        gcc \
        gdb \
        git \
        python3-dev \
        software-properties-common \
        time \
        vim \
        wget && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/*

# Install API framework
RUN apt-get update && \
    apt-get install -y \
    python3-flask

# Switch user and working directory.
USER rds
WORKDIR /home/rds
COPY [".bashrc", "/home/rds/"]

# Define default command.
CMD ["bash"]

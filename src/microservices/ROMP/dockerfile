
# Environment for the microservice ROMP.

# Pull base image.
FROM ubuntu:18.04

# Add user
RUN groupadd -g 9999 rds && \
    useradd -r -u 9999 -g rds -m -d /home/rds rds

# Install API framework
RUN apt-get update && \
    apt-get install -y \
    python3-flask \
    python3-requests

# Install packages.
RUN apt-get update && \
    apt-get install -y \
        apt-utils \
        bc \
        build-essential \
        clang \
        cmake \
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

# Add user
RUN useradd -r -u 9990 -g rds -m -d /home/awang15 awang15

# Switch user and working directory.
USER rds
WORKDIR /home/rds
ENV PATH /home/awang15/Projects/romp/spack/bin:$PATH

COPY [".spack", "/home/awang15/.spack"]
COPY ["spack", "/home/awang15/Projects/romp/spack"]
COPY [".bashrc", "/home/rds/"]

# Define default command.
CMD ["bash"]

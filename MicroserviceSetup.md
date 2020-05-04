# Set four microservices by following steps.

Download source code from our GitHub Reporsitory:

```
          git clone https://github.com/RaceDetectionService/SC20.git
          or
          git clone https://github.com/RaceDetectionService/RaceDetectionService_Server.git

```

## Setup Microservice-Archer: 

To setup Microservice-Archer, you need install Archer on you computer. The instruction for install Archer can be found here:

[Instruction for install four tools](InstallTool.md)

Run the Microserive for Archer by following commend:

```
          cd src
          cd microservices
          cd Archer
          python3 Flask_Archer.py
```

## Setup Microservice-ThreadSanitizer: 

To setup Microservice-ThreadSanitizer, you need install ThreadSanitizer on you computer. The instruction for install ThreadSanitizer can be found here:

[Instruction for install four tools](InstallTool.md)

Run the Microserive for ThreadSanitizer by following commend:

```
          cd src
          cd microservices
          cd ThreadSanitizer
          python3 Flask_TSan.py
```

## Setup Microservice-IntelInspector: 

To setup Microservice-IntelInspector, you need install Intel Inspector on you computer. The instruction for install Intel Inspector can be found here:

[Instruction for install four tools](InstallTool.md)

Run the Microserive for Intel Inspector by following commend:

```
          cd src
          cd microservices
          cd Inspector
          python3 Flask_Intellnspector.py
```

## Setup Microservice-Romp: 

To setup Microservice-Romp, you need install Romp on you computer. The instruction for install Romp can be found here:

[Instruction for install four tools](InstallTool.md)

Run the Microserive for Romp by following commend:

```
          cd src
          cd microservices
          cd ROMP
          python3 Flask_ROMP.py
```

Those four microservices run on same port by default. If you want to run those microsercive, you need run it on four different computers. Or, you can use the docker image provice by us. You can check the prvious docker instruction to set up microservice.

## Build Docker images

Instead of installing all tools manually on the host, we could also build the Docker images for easier deployment.

```bash
# get the RDS source code
git clone https://github.com/RaceDetectionService/RaceDetectionService_Server.git
```
#### Archer

```bash
# enter the RDS srouce folder first
cd src/microservices/Archer/
docker build -t rds-archer -f dockerfile .
```

#### ThreadSanitizer

```bash
# enter the RDS srouce folder first
cd src/microservices/ThreadSanitizer
docker build -t rds-tsan -f dockerfile .
```

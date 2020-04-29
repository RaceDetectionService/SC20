# Set Metaservice by following steps.

Download source code from our GitHub Reporsitory:

```
          git clone https://github.com/RaceDetectionService/SC20.git
          or
          git clone https://github.com/RaceDetectionService/RaceDetectionService_Server.git

```

Deploye Metaservice:

```
          cd src
          cd metaservice
          ./start.sh
          
```

This Metaservice was defaultly set on docker container. If you want to deplyment it on your local desktop or serve, you need make same changes for the terminal.py under src/metaservice. 

1. Change the url in line 251 to the domain name or IP Address for the machine used for Archer Microservice. Change the port as well. Change the benchmark url in line 283 to the domain name or IP Address for the machine used for Archer Microservice. Change the port as well.
1. Change the url in line 259 to the domain name or IP Address for the machine used for Inspector Microservice. Change the port as well. Change the benchmark url in line 289 to the domain name or IP Address for the machine used for Archer Microservice. Change the port as well.
1. Change the url in line 267 to the domain name or IP Address for the machine used for ThreadSanitizer Microservice. Change the port as well. Change the benchmark url in line 295 to the domain name or IP Address for the machine used for Archer Microservice. Change the port as well.
1. Change the url in line 275 to the domain name or IP Address for the machine used for Romp Microservice. Change the port as well. Change the benchmark url in line 301 to the domain name or IP Address for the machine used for Archer Microservice. Change the port as well.

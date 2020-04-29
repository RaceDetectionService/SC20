# SC20

## Deployment the RaceDetectionService(rds) enviorment to use

There two different ways to set up your RDS. You can set up RDS by yourslef on your local machine or you can set up RDS enviorment by our docker image. 

1. Set up RDS enviorment via docker

[Instruction of local deployment](deployment.md)

1. Set up RDS enviorment via your desktop or serve.

First, install four tools by following steps.

Install Archer: creat the floder for archer and archer build

```	
 	export ARCHER_BUILD=$PWD/ArcherBuild
	mkdir $ARCHER_BUILD && cd $ARCHER_BUILD

```	
get LLVM:
```	
  git clone https://github.com/llvm-mirror/llvm.git llvm_src
	cd llvm_src
	git checkout release_60
  ```	

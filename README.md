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
get Clang:
```
	cd tools
	git clone https://github.com/llvm-mirror/clang.git clang
	cd clang
	git checkout release_60
```
get Archer:
```
	cd ..
	git clone https://github.com/PRUNERS/archer.git archer
	cd ..
```
get compiler-rt support:
```
	git clone https://github.com/llvm-mirror/compiler-rt.git compiler-rt
	cd compiler-rt
	git checkout release_60
	cd ..
```
get other libaray support:
```
	git clone https://github.com/llvm-mirror/libcxx.git
	cd libcxx
	git checkout release_60
	cd ..	
	git clone https://github.com/llvm-mirror/libcxxabi.git
	cd libcxxabi
	git checkout release_60
	cd ..
	git clone https://github.com/llvm-mirror/libunwind.git
	cd libunwind
	git checkout release_60
	cd ..
```
get OpenMP libarary support:
```
	git clone https://github.com/llvm-mirror/openmp.git openmp
	cd openmp
	git checkout release_60
```
Build Archer with nijia:
```
	cd $ARCHER_BUILD
	mkdir -p llvm_bootstrap
	cd llvm_bootstrap
	sudo apt install ninja-build
	CC=$(which gcc) CXX=$(which g++) cmake -G Ninja \
	 -DCMAKE_BUILD_TYPE=Release \
	 -DLLVM_TOOL_ARCHER_BUILD=OFF \
	 -DLLVM_TARGETS_TO_BUILD=Native \
	 ../llvm_src
	ninja -j12 -l12
	cd ..
	export LD_LIBRARY_PATH="$ARCHER_BUILD/llvm_bootstrap/lib:${LD_LIBRARY_PATH}"
	export PATH="$ARCHER_BUILD/llvm_bootstrap/bin:${PATH}"
	export LLVM_INSTALL=$HOME/usr
	mkdir llvm_build && cd llvm_build
	cmake -G Ninja \
	 -D CMAKE_C_COMPILER=clang \
	 -D CMAKE_CXX_COMPILER=clang++ \
	 -D CMAKE_BUILD_TYPE=Release \
	 -D OMP_PREFIX:PATH=$LLVM_INSTALL \
	 -D CMAKE_INSTALL_PREFIX:PATH=$LLVM_INSTALL \
	 -D CLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp \
	 -D LLVM_ENABLE_LIBCXX=ON \
	 -D LLVM_ENABLE_LIBCXXABI=ON \
	 -D LIBCXXABI_USE_LLVM_UNWINDER=ON \
	 -D CLANG_DEFAULT_CXX_STDLIB=libc++ \
	 -D LIBOMP_OMPT_SUPPORT=on \
	 -D LIBOMP_OMPT_BLAME=on \
	 -D LIBOMP_OMPT_TRACE=on \
	 ../llvm_src
	ninja -j12 -l12
	ninja check-libarcher
	ninja install
```
Set up the Archer path:
```
	export PATH=${LLVM_INSTALL}/bin:${PATH}"
	export LD_LIBRARY_PATH=${LLVM_INSTALL}/lib:${LD_LIBRARY_PATH}"
```
Test Archer:
```	
 	clang-archer DRB104-nowait-barrier-orig-no.c -o myApp -larcher
	./myApp 
```

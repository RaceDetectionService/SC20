# Install four tools by following steps.

## Install Archer: 

Creat the floder for archer and archer build

```	
 	export ARCHER_BUILD=$PWD/ArcherBuild
	mkdir $ARCHER_BUILD && cd $ARCHER_BUILD

```	
Get LLVM:
```	
  	git clone https://github.com/llvm-mirror/llvm.git llvm_src
	cd llvm_src
	git checkout release_60
  ```	
Get Clang:
```
	cd tools
	git clone https://github.com/llvm-mirror/clang.git clang
	cd clang
	git checkout release_60
```
Get Archer:
```
	cd ..
	git clone https://github.com/PRUNERS/archer.git archer
	cd ..
```
Get compiler-rt support:
```
	git clone https://github.com/llvm-mirror/compiler-rt.git compiler-rt
	cd compiler-rt
	git checkout release_60
	cd ..
```
Get other libaray support:
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
Get OpenMP libarary support:
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
	export TSAN_OPTIONS="ingor_noninstrumented_modules=1"
```
Test Archer:
```	
 	clang-archer DRB104-nowait-barrier-orig-no.c -o myApp -larcher
	./myApp 
```
## Install ThreadSanitizer:

Get llvm 10.0, clang 10.0, OpenMP 10.0 and compiler-rt:
```
	wget https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/llvm-10.0.0.src.tar.xz
	wget https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/compiler-rt-10.0.0.src.tar.xz
	wget https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/openmp-10.0.0.src.tar.xz
	wger https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/clang-10.0.0.src.tar.xz
	tar xf llvm-10.0.0.src.tar.xz
	tar xf clang-10.0.0.src.tar.xz
	tar xf openmp-10.0.0.src.tar.xz
	tar xf compiler-rt-10.0.0.src.tar.xz
	mv clang-10.0.0.src llvm-10.0.0.src/tools/clang
	mv openmp-10.0.0.src llvm-10.0.0.src/projects/openmp
	mv compiler-rt-10.0.0.src llvm-10.0.0.src/projects/compiler-rt
```
Creat the floder for clang and clang build:
```
	mkdir build
 	cd build
	cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$(pwd)/../install \
	-DCLANG_OPENMP_NVPTX_DEFAULT_ARCH=sm_60 \
	-DLIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES=35,60,70 ../llvm-10.0.0.src
	make -j8
	make -j8 install
```
Build OpenMP library:
```
	cd ..
	mkdir build-openmp
	cd build-openmp
	 cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$(pwd)/../install \
	-DCMAKE_C_COMPILER=$(pwd)/../install/bin/clang \
	-DCMAKE_CXX_COMPILER=$(pwd)/../install/bin/clang++ \
	-DLIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES=35,60,70 \
	../llvm-10.0.0.src/projects/openmp
	make -j8
	make -j8 install
	cd ..
```
Set the path and enviorment:
```
	export PATH=$(pwd)/install/bin:$PATH
 	export LD_LIBRARY_PATH=$(pwd)/install/lib:$LD_LIBRARY_PATH
	export TSAN_OPTIONS="ingor_noninstrumented_modules=1"
```
Test 
```
	clang DRB001-antidep1-orig-yes.c -fopenmp -fsanitize=thread -fPIE -pie -g -o myApp
	./myApp
```
## Install ROMP
Get Special Spack and check out to romp-build branch:
```
	git clone git@github.com:zygyz/spack.git
	git checkout romp-build
```
Source Spack and Install GCC 9.6.2 via spack:
```
	export PATH='Path to spack folder that you just download'
	spack install gcc@9.6.2
```
Add your spack installed GCC 9.6.2:
	Configure the compiler option by following the steps in: https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html
```
	spack config edit compilers 
	spack compiler find
```
Install OpenMP and support library:
```
	spack install gflags %gcc@9.6.2
	spack install llvm-openmp %gcc@9.6.2
	spack install glog %gcc@9.6.2
	spack install dyninst %gcc@9.6.2
```
Install Romp:
```
	spack install romp %gcc@9.6.0
```
Set the Romp enviroment and path:
```
	export LD_LIBRARY_PATH=/path to the glog/lib:/path to the llvm-openmp-romp-mod/lib:/path to the dyninst/lib
	export DYNINSTAPI_RT_LIB=/path to the dyninist/lib/libdyninstAPI_RT.so
	export ROMP_PATH=/hpath to the romp/lib/libomptrace.so
	export PATH=/path to the romp/bin:$PATH	
```
Link your gcc and omp library to the spack installed gcc and omp:
```
	ln -s -f /path to spack gcc/bin/gcc /usr/bin/gcc
	ln -s /path to the spack installed llvm/lib/libomp.so /path to the spack installed llvm/lib/libomp.so.5
```
Test your Romp:
```
	gcc -g -fopenmp -lomp DRB001-antidep1-orig-yes.c -o test
	InstrumentMain --program=./myApp
	export ROMP_REPORT_LINE=on
	./myApp.inst
```
## Install Intel Inspector

Download inspector for linux from Intel inspector website:
https://software.intel.com/en-us/parallel-studio-xe

Install the Intel Parallel Studio. You may need a valid Intel license to install it

Source the Intel Parallel Studio:
```
	source /opt/intel/parallel_studio_xe_2020.0.088/bin/psxevars.sh
```
Set up the path and enviorment for Intel Inspector:
```
	export PATH=/opt/intel/bin:$PATH
	export PATH=/opt/intel/inspector/bin32:$PATH
```
Test Intel Inspector
```
	icc -O0 -g -fopenmp DRB001-antidep1-orig-yes.c -o myApp
	inspxe-cl  -collect ti3 -knob scope=extreme -knob stack-depth=16 -knob use-maximum-resources=true -result-dir myResult ./myApp
	inspxe-cl -report problems -result-dir Result -report-output myResult/myThreadingReport.txt
```

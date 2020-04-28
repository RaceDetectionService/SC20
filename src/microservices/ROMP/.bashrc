
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ls='ls --color=auto'
alias vi='vim'

export LD_LIBRARY_PATH=`spack location --install-dir llvm-openmp`/lib:`spack location --install-dir dyninst`/lib
export DYNINSTAPI_RT_LIB=`spack location --install-dir dyninst`/lib/libdyninstAPI_RT.so
export ROMP_PATH=`spack location --install-dir romp`/lib/libomptrace.so
export PATH=`spack location --install-dir romp`/bin:$PATH
export ROMP_REPORT_LINE=on
export ROMP_REPORT=on


#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
mkdir llvm-gcc-obj
cd llvm-gcc-obj
../llvm-gcc${LCG_package_config_version}-${LCG_llvm_config_version}.source/configure --prefix=${LCG_destbindir}  ${LCG_llvm_gcc_config_opts} --enable-shared

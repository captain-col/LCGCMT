#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd llvm-${LCG_package_config_version}.src/tools
tar xvfz ${LCG_builddir}/clang-${LCG_package_config_version}.tar.gz
mv clang-${LCG_package_config_version}.src clang
cd ..
patch -p0 < ../llvm-${LCG_package_config_version}.patch
./configure --prefix=${LCG_destbindir} --enable-optimized --with-cxx-include-root=${LCG_cxx_root} --with-c-include-dirs=${LCG_llvm_includes} --with-cxx-include-arch=x86_64-unknown-linux-gnu --with-cxx-include-32bit-dir=32 --with-cxx-include-64bit-dir=\"\"

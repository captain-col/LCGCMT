#!/bin/sh

cd ${LCG_builddir}
tar xvfj ${LCG_tarfilename}
tar xvfz valgrind_${LCG_package_config_version}_patches.tar.gz
cd valgrind-${LCG_package_config_version}
patch -p0 -i ${LCG_builddir}/valgrind_${LCG_package_config_version}_patches/valgrind-coregrind_n_segments.patch
patch -p0 -i ${LCG_builddir}/valgrind_${LCG_package_config_version}_patches/valgrind-pub-core-aspacemgr.patch
patch -p0 -i ${LCG_builddir}/valgrind_${LCG_package_config_version}_patches/valgrind-dump.patch
patch -p0 -i ${LCG_builddir}/valgrind_${LCG_package_config_version}_patches/valgrind-global.patch
./configure --prefix=${LCG_extdir}/valgrind/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_valgrind_compile_opts}

#!/bin/sh
date
cd ${LCG_builddir}/Python-${LCG_package_config_version}_shared
make

cd ${LCG_builddir}/Python-${LCG_package_config_version}_static
make CFLAGSFORSHARED=-fPIC 

if [[ $CMTCONFIG == *mac* ]]; then
    cd ${LCG_builddir}/Python-${LCG_package_config_version}_framework
    make
fi

date

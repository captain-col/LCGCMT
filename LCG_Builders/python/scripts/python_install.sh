#!/bin/sh
if [[ $CMTCONFIG == *mac* ]]; then
    cd ${LCG_builddir}/Python-${LCG_package_config_version}_framework
    make install
    # remove bin folder which contains symlinks to Python.framwork/Versions/Current/bin
    rm -rf ${LCG_destbindir}/bin
fi

cd ${LCG_builddir}/Python-${LCG_package_config_version}_shared
make install

cd ${LCG_builddir}/Python-${LCG_package_config_version}_static
make install

cd ${LCG_builddir}/Python-${LCG_package_config_version}_shared
cp Makefile ${LCG_destbindir}/lib/python${LCG_python_config_version_twodigit}/config/

cd ${LCG_destbindir}/bin
py1digit=`echo ${LCG_package_config_version} | cut -c 1`
ln -s python python${py1digit}

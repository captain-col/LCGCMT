#!/bin/sh

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}
mkdir -p ${LCG_destbindir}/bin
cp svm-train svm-predict svm-scale ${LCG_destbindir}/bin
mkdir -p ${LCG_destbindir}/include
cp smv.h ${LCG_destbindir}/include
mkdir -p ${LCG_destbindir}/src
cp smv.cpp ${LCG_destbindir}/src
mkdir -p ${LCG_destbindir}/python
cp python/*.so python/*.py python/README ${LCG_destbindir}/python
cp -r README tools ${LCG_destbindir}

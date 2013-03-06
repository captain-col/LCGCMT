#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
tar xvfz cppunit-${LCG_package_config_version}.tar.gz
cd cppunit-${LCG_cppunit_version}
patch -p1 < ../cppunit-${LCG_package_config_version}/cppunit.patch
${LCG_cppunit_compile_options}
./configure --prefix=${LCG_extdir}/CppUnit/${LCG_package_config_version}/${LCG_CMTCONFIG}

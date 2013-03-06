#!/bin/sh

cd ${LCG_builddir}/cppunit-${LCG_cppunit_version}
make install
cp ../cppunit-${LCG_package_config_version}/CppUnit_testdriver.cpp ${LCG_extdir}/CppUnit/${LCG_package_config_version}/${LCG_CMTCONFIG}/include

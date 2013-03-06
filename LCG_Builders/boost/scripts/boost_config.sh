#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd boost_${LCG_package_file_config_version}

echo "using python : ${LCG_python_version_twodigit} : ${LCG_python_root} ;" > user-config.jam
if [[ $LCG_setcpp11 == yes ]]; then
echo 'using gcc : : :  <compileflags>-std=gnu++0x ;' >> user-config.jam
fi
if [[ $CMTCONFIG == i686-* ]]; then
echo 'using gcc : : :  <linkflags>-m32 <compileflags>-m32 ;' >> user-config.jam
fi
cd tools/build/v2/
./bootstrap.sh

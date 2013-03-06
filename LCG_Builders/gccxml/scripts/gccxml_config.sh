#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
#cd gccxml
#patch -p0 < ../gccxml-${LCG_package_config_version}.diff
#cd ..
mkdir gccxml-build
cd gccxml-build
${LCG_gccxml_compile_options}
cmake ../gccxml-${LCG_package_config_version} -DCMAKE_INSTALL_PREFIX:PATH=${LCG_destbindir}

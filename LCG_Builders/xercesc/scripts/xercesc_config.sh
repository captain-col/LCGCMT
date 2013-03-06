#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd ${LCG_builddir}/xerces-c-${LCG_package_config_version}
${LCG_xercesc_compile_options}
./configure --prefix=${LCG_destbindir} ${LCG_xercesc_config_options} 

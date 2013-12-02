#!/bin/sh

package_directory=gmp-${LCG_package_config_version}

cd ${LCG_builddir}
if [ -d ${package_directory} ]; then
    echo XXXX ${LCG_builddir}/${package_directory} already exists. 
    echo XXXX Not unpacking and reconfiguring.  
    echo XXXX Remove directory to force reconfiguration.  
    exit 0
fi

tar xvfz ${LCG_tarfilename}
cd ${package_directory}

CFLAGS=" -O2 " ./configure --prefix=${LCG_extdir}/GMP/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_gmp_config_opts}

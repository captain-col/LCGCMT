#!/bin/sh

package_directory=mpfr-${LCG_package_config_version}

mkdir -p ${LCG_destbindir}
cd ${LCG_destbindir}

if [ -d ${package_directory} ]; then
    echo XXXX ${LCG_destbindir}/${package_directory} already exists. 
    echo XXXX Not unpacking and reconfiguring.  
    echo XXXX Remove directory to force reconfiguration.  
    exit 0
fi

tar xvfz ${LCG_tardir}/${LCG_tarfilename}
cd ${package_directory}

CFLAGS=" -O2 " ./configure --prefix=${LCG_destbindir} ${LCG_mpfr_config_opts}

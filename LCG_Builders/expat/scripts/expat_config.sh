#!/bin/sh

package_directory=expat-${LCG_package_config_version}

mkdir -p ${LCG_destbindirdir}
cd ${LCG_destbindirdir}

if [ -d ${package_directory} ]; then
    echo XXXX ${LCG_destbindir}/${package_directory} already exists. 
    echo XXXX Not unpacking and reconfiguring.  
    echo XXXX Remove directory to force reconfiguration.  
    exit 0
fi

tar xvfz ${LCG_tardir}/${LCG_tarfilename}
cd ${package_directory}

CFLAGS=" -O2 " ./configure --prefix=${LCG_destbindir} ${LCG_gsl_config_opts}

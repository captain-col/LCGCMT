#!/bin/sh

package_directory=gsl-${LCG_package_config_version}

mkdir -p ${LCG_destbindir}
cd ${LCG_destbindir}
if [ -d ${package_directory} ]; then
    echo XXXX ${LCG_builddir}/${package_directory} already exists. 
    echo XXXX Not unpacking and reconfiguring.  
    echo XXXX Remove directory to force reconfiguration.  
    exit 0
fi

tar xvfz ${LCG_tardir}/${LCG_tarfilename}
cd ${package_directory}

CFLAGS="${LCG_extra_cflags}" ./configure --prefix=${LCG_destbindir} ${LCG_gsl_config_opts}

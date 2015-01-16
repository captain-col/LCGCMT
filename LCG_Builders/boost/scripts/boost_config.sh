#!/bin/sh

package_directory=boost_${LCG_file_config_version}

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

#./bootstrap.sh --prefix=${LCG_destdir} \
#    --without-libraries=${LCG_boost_with_libraries}

./bootstrap.sh  --prefix=${LCG_destdir}

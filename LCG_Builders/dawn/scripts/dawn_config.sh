#!/bin/sh

package_directory=dawn_${LCG_package_config_version}

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

rm dev_control.h
cat > dev_control.h << EOF

#if !defined DEV_CONTROL_H
#define DEV_CONTROL_H

#define USE_OPEN_GL
#define USE_XWIN
#define USE_UNIX
//#define USE_SOCKET
#endif

EOF

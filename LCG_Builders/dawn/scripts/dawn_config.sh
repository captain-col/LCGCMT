#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}

cd dawn_${LCG_package_config_version}
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

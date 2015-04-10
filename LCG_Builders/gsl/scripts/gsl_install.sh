#!/bin/sh

cd ${LCG_destbindir}/gsl-${LCG_package_config_version}

if [ -d ../bin -a -d ../lib -a -d ../include -a -d ../share ]; then
    echo XXXX No need to install gsl-${LCG_package_config_version}
    echo XXXX Remove installation to force re-installation
    exit 0
fi

make install

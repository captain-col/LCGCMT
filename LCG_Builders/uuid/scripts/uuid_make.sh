#!/bin/sh
cd ${LCG_builddir}
export PATH=`pwd`:$PATH
cd e2fsprogs-${LCG_package_config_version}
make 

#!/bin/sh

cd ${LCG_builddir}
tar xvzf ${LCG_tarfilename}
cd numpy-${LCG_package_config_version}
#patch -p0 < system_info.py.diff

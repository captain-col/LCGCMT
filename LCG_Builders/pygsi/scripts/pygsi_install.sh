#!/bin/sh

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}
mkdir -p $INSTALLPATH
python setup.py install --prefix ${LCG_destbindir}

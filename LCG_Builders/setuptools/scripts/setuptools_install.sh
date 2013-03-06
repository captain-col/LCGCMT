#!/bin/sh

cd ${LCG_builddir}/setuptools-${LCG_package_config_version}
mkdir -p ${LCG_destbindir}/lib/python${LCG_Python_config_version_twodigit}/site-packages
python setup.py install --prefix ${LCG_destbindir}

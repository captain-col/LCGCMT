#!/bin/sh

cd ${LCG_builddir}/processing-${LCG_package_config_version}
python setup.py install --prefix ${LCG_destbindir}

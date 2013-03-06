#!/bin/sh

cd ${LCG_builddir}/lxml-${LCG_package_config_version}
python setup.py install --prefix ${LCG_destbindir}


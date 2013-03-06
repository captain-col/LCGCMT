#!/bin/sh

cd ${LCG_builddir}/Genshi-${LCG_package_config_version}
python setup.py install --prefix ${LCG_destbindir}


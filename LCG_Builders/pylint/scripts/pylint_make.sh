#!/bin/sh

cd ${LCG_builddir}/logilab-astng-${logilab_astng_config_version}
python setup.py install --prefix ${LCG_destbindir}

cd ${LCG_builddir}/logilab-common-${logilab_common_config_version}
python setup.py install --prefix ${LCG_destbindir}

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}
python setup.py build

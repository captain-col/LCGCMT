#!/bin/sh

cd ${LCG_builddir}/MySQL-python-${LCG_package_config_version}
python setup.py install --root ${LCG_destbindir} --prefix ""

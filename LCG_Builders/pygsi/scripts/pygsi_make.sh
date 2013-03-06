#!/bin/sh
cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}
python setup.py build

#!/bin/sh

cd ${LCG_builddir}/storm-${LCG_package_config_version}
${LCG_storm_compile_options}
python setup.py build

#!/bin/sh

cd ${LCG_builddir}/setuptools-${LCG_package_config_version}
${LCG_setuptools_compile_options}
python setup.py build

#!/bin/sh

cd ${LCG_builddir}/pytest-$LCG_package_config_version
${LCG_pytest_compile_options}
python setup.py build

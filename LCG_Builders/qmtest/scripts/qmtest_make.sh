#!/bin/sh

cd ${LCG_builddir}/qmtest-${LCG_package_config_version}
${LCG_qmtest_compile_options}
python setup.py build 

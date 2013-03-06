#!/bin/sh

cd ${LCG_builddir}/pyparsing-${LCG_package_config_version}
${LCG_pyparsing_compile_options}
python setup.py build

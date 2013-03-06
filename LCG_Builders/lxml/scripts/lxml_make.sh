#!/bin/sh

cd ${LCG_builddir}/lxml-${LCG_package_config_version}
${LCG_lxml_compile_options}
python setup.py build

#!/bin/sh

cd ${LCG_builddir}/Genshi-${LCG_package_config_version}
${LCG_genshi_compile_options}
python setup.py build

#!/bin/sh

cd ${LCG_builddir}/pydot-${LCG_package_config_version}
${LCG_pydot_compile_options}
python setup.py build

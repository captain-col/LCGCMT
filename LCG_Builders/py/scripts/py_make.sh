#!/bin/sh

cd ${LCG_builddir}/py-$LCG_package_config_version
${LCG_py_compile_options}
python setup.py build

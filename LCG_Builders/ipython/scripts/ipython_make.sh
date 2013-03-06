#!/bin/sh

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}
${ipython_compile_options}
python setup.py build

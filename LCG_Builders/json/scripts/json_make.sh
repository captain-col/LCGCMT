#!/bin/sh

cd ${LCG_builddir}/simplejson-${LCG_package_config_version}
${LCG_json_compile_options}
python setup.py build

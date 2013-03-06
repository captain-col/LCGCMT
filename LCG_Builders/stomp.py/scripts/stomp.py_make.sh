#!/bin/sh

cd ${LCG_builddir}/stomp.py-$LCG_package_config_version
${LCG_stomppy_compile_options}
python setup.py build

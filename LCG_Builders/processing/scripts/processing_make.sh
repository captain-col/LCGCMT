#!/bin/sh

cd ${LCG_builddir}/processing-${LCG_package_config_version}
${LCG_processing_compile_options}
python setup.py build

#!/bin/sh
cd ${LCG_builddir}/PyXML-${LCG_package_config_version}
${LCG_pyxml_compile_options}
python setup.py build

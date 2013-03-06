#!/bin/sh

cd ${LCG_builddir}/4Suite-XML-${LCG_package_config_version}
LDFLAGS="-L${LCG_python_libdir}" python setup.py build

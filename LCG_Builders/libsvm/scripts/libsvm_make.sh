#!/bin/sh

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}
make
cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}/python
make PYTHON_INCLUDEDIR=${LCG_python_incdir} all LDFLAGS="${LCG_libsvm_ldflags}"


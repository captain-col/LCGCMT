#!/bin/sh

cd ${LCG_builddir}/sympy-${LCG_sympy_native_version}
python setup.py install --prefix ${LCG_destbindir}

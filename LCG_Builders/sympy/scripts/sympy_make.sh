#!/bin/sh

cd ${LCG_builddir}/sympy-${LCG_sympy_native_version}
${LCG_sympy_compile_options}
python setup.py build

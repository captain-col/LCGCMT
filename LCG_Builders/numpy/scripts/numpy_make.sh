#!/bin/sh

cd ${LCG_builddir}/numpy-${LCG_package_config_version}
${LCG_py_compile_options}

if [[ $CMTCONFIG == i686-* ]]; then
   find ./ -name *.py -exec sed -i 's/-shared/-m32 -shared/g' {} \;
fi

python setup.py build

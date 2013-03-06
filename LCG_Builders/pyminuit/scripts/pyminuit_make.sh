#!/bin/sh

export VERSION=`cmt show macro_value minuit_config_version`
cd ${LCG_builddir}/pyminuit2-${LCG_pyminuit_native_version}
${LCG_pyminuit_compile_options}

python setup.py build 

#!/bin/sh

cd ${LCG_builddir}/pyminuit2-${LCG_pyminuit_native_version}
export VERSION=`cmt show macro_value minuit_config_version`
python setup.py install --prefix ${LCG_destbindir}

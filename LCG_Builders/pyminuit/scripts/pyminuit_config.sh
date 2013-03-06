#!/bin/sh

cd ${LCG_builddir}
tar xvzf ${LCG_tarfilename}
cd pyminuit2-${LCG_pyminuit_native_version}
patch -p0 <../pyminuit2.diff

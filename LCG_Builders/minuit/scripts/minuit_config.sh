#!/bin/sh

cd ${LCG_builddir}
tar xvzf ${LCG_tarfilename}
cd Minuit2-${LCG_minuit_config_version}
./configure --prefix=${LCG_destbindir}

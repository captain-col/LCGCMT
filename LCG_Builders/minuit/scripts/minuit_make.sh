#!/bin/sh

cd ${LCG_builddir}/Minuit2-${LCG_minuit_config_version}
${LCG_minuit_compile_options}
make

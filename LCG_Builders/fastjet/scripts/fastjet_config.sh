#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
tar xvfz ${LCG_fastjet_FastPrune_plugin}
tar xvfz ${LCG_fastjet_VRPlugins_plugin}
tar xvfz ${LCG_fastjet_trimming_plugin}
tar xvfz ${LCG_fastjet_tools}
cd ${LCG_builddir}/fastjet-${LCG_package_config_version}
${LCG_fastjet_compile_options}
./configure --prefix=${LCG_destbindir} --enable-shared --enable-allplugins

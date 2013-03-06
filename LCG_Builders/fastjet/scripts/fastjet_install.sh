#!/bin/sh

cd ${LCG_builddir}/fastjet-${LCG_package_config_version}
make install
export CPATH=${LCG_destbindir}/include
export PATH=${LCG_destbindir}/bin:$PATH

cd ${LCG_builddir}/TrimmingPlugin
make
rsync -avz lib/libfjtrimmingplugins.* ${LCG_destbindir}/lib
rsync -avz *.hh ${LCG_destbindir}/include/

cd ${LCG_builddir}/VRPlugins
make
rsync -avz libfjplugins.* ${LCG_destbindir}/lib
rsync -avz */*.hh ${LCG_destbindir}/include/

cd ${LCG_builddir}/FastPrune-0.4.3
make
rsync -avz lib/libFastPrunePlugin.* ${LCG_destbindir}/lib
rsync -avz include/fastjet/*.hh ${LCG_destbindir}/include/fastjet

cd ${LCG_builddir}
rsync -avz *.hh ${LCG_destbindir}/include/

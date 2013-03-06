#!/bin/sh

cd ${LCG_builddir}/PyQt-${LCG_pyqt_plat_name}-gpl-${LCG_package_config_version}

if [[ $CMTCONFIG == i686-* ]]; then
   find ./ -name Makefile -exec sed -i 's/LFLAGS = -shared/LFLAGS = -m32 -shared/g' {} \;
   find ./ -name Makefile -exec sed -i 's/LFLAGS = -Wl/LFLAGS = -m32 -Wl/g' {} \;
fi

make


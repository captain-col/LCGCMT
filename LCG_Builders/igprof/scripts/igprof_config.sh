#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd igprof-${LCG_package_config_version}
cmake -DCMAKE_INSTALL_PREFIX:PATH=${LCG_destbindir} -DUNWIND_INCLUDE_DIR:PATH=${UNWIND_INCLUDE_DIR} -DUNWIND_LIBRARY:FILEPATH=${UNWIND_LIBRARY}


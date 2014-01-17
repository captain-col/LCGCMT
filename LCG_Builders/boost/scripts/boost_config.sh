#!/bin/sh

package_directory=boost_${LCG_file_config_version}

cd ${LCG_builddir}

tar xvfz ${LCG_tarfilename}
cd ${package_directory}

#./bootstrap.sh --prefix=${LCG_destdir} \
#    --without-libraries=${LCG_boost_with_libraries}

./bootstrap.sh  --prefix=${LCG_destdir}

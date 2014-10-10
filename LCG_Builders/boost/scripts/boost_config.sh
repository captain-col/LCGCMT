#!/bin/sh

package_directory=boost_${LCG_file_config_version}

mkdir -p ${LCG_destbindir}
cd ${LCG_destbindir}

tar xvfz ${LCG_tardir}/${LCG_tarfilename}
cd ${package_directory}

#./bootstrap.sh --prefix=${LCG_destdir} \
#    --without-libraries=${LCG_boost_with_libraries}

./bootstrap.sh  --prefix=${LCG_destdir}

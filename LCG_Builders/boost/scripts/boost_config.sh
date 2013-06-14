#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd boost_${LCG_package_file_config_version}

./bootstrap.sh --prefix=${LCG_destdir} \
    --with-libraries=${LCG_boost_with_libraries}

#!/bin/sh


cd ${LCG_builddir}
tar xvjf ${LCG_tarfilename}
cd qwt-${LCG_package_config_version}

if [ ! -f qwtconfig.pri ]; then
    echo "Error, unpacked sourced does not contain a configuration file tar file qwtconfig.pri"
    return 1
fi

cat qwtconfig.pri |sed 's#QWT_INSTALL_PREFIX *= *.*$#QWT_INSTALL_PREFIX='"${LCG_destbindir}"'#' > qwtconfig.pri_tmp && mv -f qwtconfig.pri_tmp qwtconfig.pri
if [ $? != 0 ]; then
    echo "Errors encountered while modifying qwtconfig.pri"
    return 1
fi

qmake ${QMAKE_SPEC}

#./configure --prefix=${LCG_destbindir} ${LCG_coin3d_config_opts}

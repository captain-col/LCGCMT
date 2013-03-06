#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
mkdir xrootd_build
cd xrootd_build
cmake ../xrootd-${LCG_package_config_version} -DCMAKE_INSTALL_PREFIX:PATH=${LCG_destbindir} -DENABLE_PERL=FALSE -DENABLE_FUSE=FALSE -DENABLE_CRYPTO=TRUE -DENABLE_KRB5=TRUE -DENABLE_READLINE=TRUE


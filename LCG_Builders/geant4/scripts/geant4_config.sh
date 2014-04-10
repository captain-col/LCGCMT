#!/bin/sh
# This config script is aimed at a cmake package.  It should be
# customized for the package being built.

# This should be customized to here the package should be built.  The
# default is to install in the LCG_destbindir so that the build
# directory is near the installation directory.  It needs to be the
# LCG_destbindir since many autoconf and related packages compile in
# the source directories.  Make sure the destination exists, and then
# go there.
mkdir -p ${LCG_destdir}
cd ${LCG_destdir}

# This needs to be set to the installation prefix
LOCAL_install=${LCG_destbindir}
mkdir -p ${LOCAL_install}

# This needs to be set to where the package will be built
LOCAL_build=${LCG_destbindir}/build
mkdir -p ${LOCAL_build}

# This has to be set to the directory that the tar file will unpack
# into when tar is run from the ${LCG_destdir} directory.  If upstream
# changes the top-level tar directory, this will need to be changed.
LOCAL_src=${LCG_destdir}/${LCG_srcdir}

# If the source hasn't been unpacked, then unpack it.  This check
# helps make sure that redoing "make pkg_config" doesn't force a
# rebuilt.
if [ ! -d ${LOCAL_src} -a -f  ${LCG_tardir}/${LCG_tarfilename} ]; then 
    tar xvfz ${LCG_tardir}/${LCG_tarfilename}
fi

# Unpack the geant4 data files
cd ${LCG_destdir}/..
if [ ! -d share ]; then
    mkdir share
fi
cd share

for data in $(echo ${LCG_datafiles} | sed 's/;/ /g') ; do
    tar xvzf ${LCG_tardir}/${data}
done 

cd ${LOCAL_build}
cmake -DCMAKE_INSTALL_PREFIX=${LOCAL_install} ${LCG_build_options} ${LOCAL_src}


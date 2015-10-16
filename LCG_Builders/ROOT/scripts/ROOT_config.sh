#!/bin/sh
# This config script is aimed at a cmake package.  It should be
# customized for the package being built.

# This should be customized to here the package should be built.  The
# default is to install in the LCG_destbindir so that the build
# directory is near the installation directory.  It needs to be the
# LCG_destbindir since many autoconf and related packages compile in
# the source directories.  Make sure the destination exists.
mkdir -p ${LCG_destdir}

# This needs to be set to the installation prefix
LOCAL_install=${LCG_destbindir}
mkdir -p ${LOCAL_install}

# This has to be set to the directory that the tar file will unpack
# into when tar is run from the ${LCG_destdir} directory.  If upstream
# changes the top-level tar directory, this will need to be changed.
LOCAL_src=${LCG_destdir}/${LCG_srcdir}

# If the source hasn't been unpacked, then unpack it.  This check
# helps make sure that redoing "make pkg_config" doesn't force a
# rebuilt.
cd ${LCG_destdir}
if [ ! -d ${LOCAL_src} -a -f  ${LCG_tardir}/${LCG_tarfilename} ]; then 
    tar xvfz ${LCG_tardir}/${LCG_tarfilename}
else
    echo XXXX ${LCG_src} already exists, so not unpacking.
    echo XXXX Remove directory to force new source.
fi

# This needs to be set to where the package will be built
LOCAL_build=${LOCAL_src}-build
mkdir -p ${LOCAL_build}

# Make sure the ROOTSYS variable isn't set for the build.
if [ ${#ROOTSYS} != 0 ]; then
    unset ROOTSYS
fi
	   
# Go to the build area.
cd ${LOCAL_build}

if [ -e CMakeCache.txt -a CMakeCache.txt \
	-nt ${LCG_package_root}/cmt/requirements ]; then
    echo XXXX No need to rerun configuration
    exit 0
fi
exit 0

cmake -DCMAKE_INSTALL_PREFIX=${LOCAL_install} ${LCG_build_options} ${LOCAL_src}



#!/bin/sh

# This config script is aimed at an autoconf package.  It should be
# customized for the package being built.

# This should be customized to here the package should be built.  The
# default is to build in the LCG_destbindir so that the build
# directory is near the installation directory.  It needs to be the
# LCG_destbindir since many autoconf and related packages compile in
# the source directories.  Make sure the destination exists, and then
# go there.
mkdir -p ${LCG_destbindir}
cd ${LCG_destbindir}

# This has to be set to the directory that the tar file will unpack
# into.  If upstream changes the top-level tar directory, this will
# need to be changed.
LOCAL_srcdir=${PWD}/${LCG_srcdir}

# If the source hasn't been unpacked, then unpack it.  This check
# helps make sure that redoing "make pkg_config" doesn't force a
# rebuilt.
if [ ! -d ${LOCAL_srcdir} -a -f  ${LCG_tardir}/${LCG_tarfilename} ]; then 
	tar xvfz ${LCG_tardir}/${LCG_tarfilename}
fi

cd ${LOCAL_srcdir}
if [ -f config.status ]; then
    echo "WARNING: ${LCG_package} already configured."
    echo "WARNING: Remove ${PWD}/config.status to reconfig."
    exit 0
fi

COVLD=""
#If coverage testing is configured, configure ROOT with differend
#linker. This linker just calls g++ with lgcov at the end.
if [[ ! -z "$GCOV_TOOL" ]];then
	COVLD="--with-ld=${LCG_package_root}/scripts/root_gcovld.sh"
fi

# Run configure
eval "./configure ${LCG_ROOT_CONFIG_ARCH} ${LCG_ROOT_CONFIG_OPTIONS} ${COVLD}"

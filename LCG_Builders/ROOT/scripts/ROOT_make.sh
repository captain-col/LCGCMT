#!/bin/sh
#
# Script to handle a cmake configured package.  This has been
# customized for ROOT.

# This has to be set to the directory that the tar file will unpack
# into when tar is run from the ${LCG_destdir} directory.  If upstream
# changes the top-level tar directory, this will need to be changed.
LOCAL_src=${LCG_destdir}/${LCG_srcdir}

# This needs to be set to where the package will be built
LOCAL_build=${LOCAL_src}-build

# Make sure the ROOTSYS variable isn't set for the build.
if [ ${#ROOTSYS} != 0 ]; then
    unset ROOTSYS
fi

# Make doubly sure the ~/.rootrc file is not read.  This is also set
# in the requirements to make the build consistent, but it ABSOLUTELY
# can not be set here, so be pedandic.
export ROOTENV_NO_HOME
ROOTENV_NO_HOME=1

# Go to the build directory and run make.  The build directory must
# match LOCAL_build in the config script.
if ! cmake --build ${LOCAL_build} -- -k -j4; then
    echo Error building ROOT.
    exit 1
fi

#!/bin/sh
#
# Script to handle a cmake configured package.  This has been
# customized for geant4.
#

# This has to be set to the directory that the tar file will unpack
# into when tar is run from the ${LCG_destdir} directory.  If upstream
# changes the top-level tar directory, this will need to be changed.
LOCAL_src=${LCG_destdir}/${LCG_srcdir}

# This needs to be set to where the package will be built
LOCAL_build=${LOCAL_src}-build

# Go to the build directory and run make.  The build directory must
# match LOCAL_build in the config script.
cd ${LOCAL_build}
make -j


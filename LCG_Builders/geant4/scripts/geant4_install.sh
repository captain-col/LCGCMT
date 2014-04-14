#!/bin/sh
#
# Script to handle a cmake configured package.  This has been
# customized for geant4.
#
# Go to the build directory and run make.  The build directory must
# match LOCAL_build in the config script.
cd ${LCG_destbindir}/build
make install

# Make sure that the lib64 that GEANT4 sometimes installs into is also in lib.
cd ${LCG_destbindir}
if [ ! -d lib ]; then
    if [ -d lib64 ]; then
	ln -s lib64 lib
    fi
fi

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

cd ${LOCAL_build}
make install

# Make sure that the lib64 that GEANT4 sometimes installs into is also in lib.
cd ${LCG_destbindir}
if [ ! -d lib ]; then
    if [ -d lib64 ]; then
	ln -s lib64 lib
    fi
fi

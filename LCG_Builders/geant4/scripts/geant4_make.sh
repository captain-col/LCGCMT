#!/bin/sh
#
# Script to handle a cmake configured package.  This has been
# customized for geant4.
#

# Set the maximum load during the job.  This can be overridden in the
# environment.
if [ "x$LCG_MAX_LOAD" = "x" ]; then
    LCG_MAX_LOAD=1.0
fi
echo Limit load to ${LCG_MAX_LOAD}

# Go to the build directory and run make.  The build directory must
# match LOCAL_build in the config script.
cd ${LCG_destbindir}/build
make -l ${LCG_MAX_LOAD} -j


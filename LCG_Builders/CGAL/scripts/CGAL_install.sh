#!/bin/sh
#
# Script to handle a cmake configured package.  This has been
# customized for cgal.
#
# Go to the build directory and run make.  The build directory must
# match LOCAL_build in the config script.
cd ${LCG_destbindir}/build
make install

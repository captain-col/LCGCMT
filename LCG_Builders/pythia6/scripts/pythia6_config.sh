#!/bin/sh

# Make sure the directory structures exist.

# This should be customized to here the package should be built.  The
# default is to install in the LCG_destbindir so that the build
# directory is near the installation directory.
mkdir -p ${LCG_destbindir}
cd ${LCG_destbindir}


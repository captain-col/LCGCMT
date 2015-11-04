#!/bin/sh

# This has to be set to the directory that the tar file was unpacked.
# If upstream changes the top-level tar directory, this will need to
# be changed.  In the case of some builder that modify the source
# directory, this should be inside the machine specific directory.
LOCAL_src=${LCG_destbindir}/cmake-${LCG_package_config_version}

# This needs to be set to where the package will be built.  This might
# be the same as the source directory.
LOCAL_build=${LOCAL_src}

cd ${LOCAL_build}
make install

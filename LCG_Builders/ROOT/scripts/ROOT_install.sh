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
	   
# Go to the build directory and run make install.
cd ${LOCAL_build}
cmake --build ${LOCAL_build} -- -k install


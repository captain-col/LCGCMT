#!/bin/sh
# This config script is aimed at a cmake package.  It should be
# customized for the package being built.

# This should be customized to the base directory for the package
# installation. All of the version specific files will be rooted from
# here.
mkdir -p ${LCG_destdir}

# The location of the machine specific installation directory.  This
# is usually set to LCG_destbindir, and must exist.
LOCAL_install=${LCG_destbindir}
mkdir -p ${LOCAL_install}

# This has to be set to the directory that the tar file will unpack
# into when tar is run.  Tar is usually run from ${LCG_destdir}
# directory, but if the compilation modifies the source directory,
# this needs to be ${LCG_destbindir}.  If upstream changes the
# top-level tar directory, this will need to be changed.  In the case
# of some builder that modify the source directory, this should be
# inside the machine specific directory.
LOCAL_src=${LCG_destdir}/${LCG_srcdir}

# If the source hasn't been unpacked, then unpack it.  This check
# helps make sure that redoing "make pkg_config" doesn't force a
# rebuilt.  Change directory to the right directory to get the source
# unpacked into LOCAL_src (usually LCG_destdir, or LCG_destbindir).
cd ${LCG_destdir}
if [ ! -d ${LOCAL_src} -a -f  ${LCG_tardir}/${LCG_tarfilename} ]; then 
    tar xvfz ${LCG_tardir}/${LCG_tarfilename}
else
    echo XXXX ${LOCAL_src} already exists, so not unpacking.
    echo XXXX Remove directory to force new source.
fi

# This needs to be set to where the package will be built.  This might
# be the same as the source directory.
LOCAL_build=${LOCAL_src}-build
mkdir -p ${LOCAL_build}

# Make sure the ROOTSYS variable isn't set for the build.
if [ ${#ROOTSYS} != 0 ]; then
    unset ROOTSYS
fi
	   
# Go to the build area.
cd ${LOCAL_build}

if [ -e CMakeCache.txt -a CMakeCache.txt \
	-nt ${LCG_package_root}/cmt/requirements ]; then
    echo XXXX No need to rerun configuration
    exit 0
fi

cmake -DCMAKE_INSTALL_PREFIX=${LOCAL_install} ${LCG_build_options} ${LOCAL_src}



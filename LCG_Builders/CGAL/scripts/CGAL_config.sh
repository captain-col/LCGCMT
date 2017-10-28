#!/bin/sh
# This config script is aimed at a cmake package.  It should be
# customized for the package being built.

# This should be customized to the base directory for the package
# installation. All of the version specific files will be rooted from
# here.
LOCAL_dest=${LCG_destdir}

# The location of the machine specific installation directory.  This
# is usually set to LCG_destbindir, and must exist.
LOCAL_install=${LCG_destbindir}

# This has to be set to the directory that the tar file will unpack
# into when tar is run from the ${LCG_destdir} directory.  If upstream
# changes the top-level tar directory, this will need to be changed.
LOCAL_src=${LOCAL_dest}/CGAL-${LCG_package_config_version}

# This needs to be set to where the package will be built
LOCAL_build=${LOCAL_src}-build

mkdir -p ${LOCAL_dest}
mkdir -p ${LOCAL_install}
mkdir -p ${LOCAL_build}

# If the source hasn't been unpacked, then unpack it.  This check
# helps make sure that redoing "make pkg_config" doesn't force a
# rebuilt.
cd ${LOCAL_dest}
if [ ! -d ${LOCAL_src} -a -f  ${LCG_tardir}/${LCG_tarfilename} ]; then 
    tar xvfz ${LCG_tardir}/${LCG_tarfilename}
fi

cd ${LOCAL_build}
cmake -DCMAKE_INSTALL_PREFIX=${LOCAL_install} ${LCG_build_options} ${LOCAL_src}

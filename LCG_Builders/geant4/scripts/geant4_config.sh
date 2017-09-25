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

# This needs to be set to where the package will be built
LOCAL_build=${LCG_destbindir}/build
mkdir -p ${LOCAL_build}

# This has to be set to the directory that the tar file will unpack
# into when tar is run.  Tar is usually run from ${LCG_destdir}
# directory, but if the compilation modifies the source directory,
# this needs to be ${LCG_destbindir}.  If upstream changes the
# top-level tar directory, this will need to be changed.  In the case
# of some builder that modify the source directory, this should be
# inside the machine specific directory.
LOCAL_src=${LCG_destdir}/${LCG_srcdir}

# This needs to be set to where the package will be built.  This might
# be the same as the source directory.
LOCAL_build=${LOCAL_src}-build
mkdir -p ${LOCAL_build}

# This is where the data files should be installed.
LOCAL_data=${LCG_destdir}/share
# Unpack the geant4 data files
if [ ! -d ${LOCAL_data} ]; then
    mkdir -p ${LOCAL_data}
fi

cd ${LOCAL_data}
for data in $(echo ${LCG_datafiles} | sed 's/;/ /g') ; do
    data_dir=$(tar tzf ${LCG_tardir}/${data} | head -1)
    if [ ! -d ${data_dir} ]; then
	tar xvzf ${LCG_tardir}/${data}
    fi
done 

# If the source hasn't been unpacked, then unpack it.
if [ ! -d ${LOCAL_src} -a -f  ${LCG_tardir}/${LCG_tarfilename} ]; then 
    cd ${LCG_destdir}
    tar xvfz ${LCG_tardir}/${LCG_tarfilename}
fi

cd ${LOCAL_build}
cmake -DCMAKE_INSTALL_PREFIX=${LOCAL_install} ${LCG_build_options} ${LOCAL_src}


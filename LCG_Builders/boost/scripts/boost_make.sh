#!/bin/sh

# This should be customized to the base directory for the package
# installation. All of the version specific files will be rooted from
# here.
LOCAL_dest=${LCG_destdir}

# The location of the machine specific installation directory.  This
# is usually set to LCG_destbindir, and must exist.
LOCAL_install=${LCG_destbindir}

# This has to be set to the directory that the tar file will unpack
# into when tar is run.  Tar is usually run from ${LCG_destdir}
# directory, but if the compilation modifies the source directory,
# this needs to be ${LCG_destbindir}.  If upstream changes the
# top-level tar directory, this will need to be changed.  In the case
# of some builder that modify the source directory, this should be
# inside the machine specific directory.
LOCAL_src=${LOCAL_dest}/boost_${LCG_file_config_version}

# This needs to be set to where the package will be built.  For some
# packages that modify the source directory, this might be the same as
# the source directory, but it's usually "parallel" to the source with
# a suffix "-build".
# BOOST NEEDS TO BE BUILT IN THE SRC DIRECTORY!!!!!!!
LOCAL_build=${LOCAL_src}

# MAKE SURE THAT THE LCG_Builders/boost/setup.sh script was run
if [ "x${LCG_file_config_version}" = "x" ]; then
    echo The local cmt setup must have been run.
    exit 1
fi

cd ${LOCAL_build}

${LCG_bjam_bin} ${LCG_boost_jam_opts} \
    ${LCG_boost_compile_options} \
    --toolset=${LCG_boost_toolset}

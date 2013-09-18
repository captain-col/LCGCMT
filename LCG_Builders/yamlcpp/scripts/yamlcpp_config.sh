#!/bin/sh

# This is the directory where source will be untarred relative to the
# LCG_builddir.  
install_directory=yamlcpp/${LCG_package_config_version}/${LCG_CMTCONFIG}

# This is the directory the tar file will unpack the source into and
# it's relative to the install_directory
package_directory=yaml-cpp

cd ${LCG_builddir}
if [ ! -d ${install_directory} ]; then
    mkdir -p ${install_directory}
fi
cd ${install_directory}

if [ -d ${package_directory} ]; then
    echo XXXX ${LCG_builddir}/${package_directory} already exists. 
    echo XXXX Not unpacking and reconfiguring.  
    echo XXXX Remove directory to force reconfiguration.  
    exit 0
fi

# Unpack the source.  This  ends up in 
# ${LCG_builddir}/${install_directory}/${package_directory} 
tar xvfz ${LCG_builddir}/${LCG_tarfilename}
LOCAL_src=${LCG_builddir}/${install_directory}/${package_directory}

# This needs to be set to where the package will be built
LOCAL_build=${LCG_builddir}/${install_directory}/build
mkdir -p ${LOCAL_build}

# This is where the package will be installed.
LOCAL_install=${LCG_builddir}/${install_directory}

cd ${LOCAL_build}
cmake -DCMAKE_INSTALL_PREFIX=${LOCAL_install} ${LCG_yamlcpp_config_opts} ${LOCAL_src}

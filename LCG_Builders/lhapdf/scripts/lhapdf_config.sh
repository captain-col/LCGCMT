#!/bin/sh

# This is the directory where source will be untarred. 
install_directory=lhapdf/${LCG_package_config_version}/${LCG_CMTCONFIG}

# This is the directory the tar file will unpack the source into and
# it's relative to the install_directory
package_directory=LHAPDF-${LCG_package_config_version}

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

tar xvfz ${LCG_builddir}/${LCG_tarfilename}
cd ${package_directory}

./configure --prefix=${LCG_extdir}/${install_directory} ${LCG_lhapdf_config_opts}

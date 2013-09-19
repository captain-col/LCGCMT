#!/bin/sh

# This is the directory where source will be untarred. 
install_directory=genie/${LCG_package_config_version}/${LCG_CMTCONFIG}

# This is the directory the tar file will unpack the source into and
# it's relative to the install_directory
package_directory=Genie-${LCG_package_config_version}

cd ${LCG_builddir}
if [ ! -d ${install_directory} ]; then
    mkdir -p ${install_directory}
fi
cd ${install_directory}

if [ -d ${package_directory} ]; then
    echo XXXX ${LCG_builddir}/${package_directory} already exists. 
    echo XXXX Not unpacking.  Remove directory to force unpack.  
    # exit 0
fi

tar xvfz ${LCG_builddir}/${LCG_tarfilename}
cd ${package_directory}

GENIE=${PWD} ./configure --prefix=${LCG_extdir}/${install_directory} ${LCG_genie_config_opts}

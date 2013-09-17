#!/bin/sh

# The script directory
script_directory=${LCG_package_root}/scripts

# This is the directory where source will be untarred. 
install_directory=pythia6/${LCG_CMTCONFIG}

# This is the directory the tar file will unpack the source into and
# it's relative to the install_directory
package_directory=${LCG_package_config_version}

cd ${LCG_builddir}
cd ${install_directory}

if [ -d ${package_directory} ]; then
    echo XXXX ${LCG_builddir}/${package_directory} already exists. 
    echo XXXX Remove directory to force rebuild.  
    exit 0
fi

# Build the package.  This also downloads the source.
${script_directory}/build_pythia6.sh ${LCG_package_config_version}

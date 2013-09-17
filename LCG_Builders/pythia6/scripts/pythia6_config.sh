#!/bin/sh

# Make sure the directory structures exist.

# The script directory
script_directory=${LCG_package_root}/scripts

# This is the directory where source will be untarred. 
install_directory=pythia6/${LCG_CMTCONFIG}

# This is the directory the tar file will unpack the source into and
# it's relative to the install_directory
package_directory=${LCG_package_config_version}

cd ${LCG_builddir}
if [ ! -d ${install_directory} ]; then
    mkdir -p ${install_directory}
fi
cd ${install_directory}


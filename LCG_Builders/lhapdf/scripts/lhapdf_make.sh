#!/bin/sh

# This is the directory where source will be untarred. 
install_directory=lhapdf/${LCG_package_config_version}/${LCG_CMTCONFIG}

# This is the directory the tar file will unpack the source into and
# it's relative to the install_directory
package_directory=lhapdf-${LCG_package_config_version}

# Go to the source directory.
cd ${LCG_builddir}/${install_directory}/${package_directory}

# Build the package.
make


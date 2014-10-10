#!/bin/sh

package_directory=gmp-${LCG_package_config_version}
cd ${LCG_destbindir}/${package_directory}

make install

#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd Python-${LCG_package_config_version}
./configure --prefix=${LCG_destbindir} ${LCG_python_config_post_opts}


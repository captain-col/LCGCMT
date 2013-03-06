#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd sip-${LCG_package_config_version}
sip_dest_dir=${LCG_destbindir}
${LCG_sip_compile_options}
python ./configure.py -b ${sip_dest_dir}/bin -d ${sip_dest_dir}/lib/python${LCG_python_config_version_twodigit}/site-packages -e ${sip_dest_dir}/include/python${LCG_python_config_version_twodigit} -v ${sip_home}/share/sip ${LCG_sip_compile_options}

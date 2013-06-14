#!/bin/sh

cd ${LCG_builddir}/boost_${LCG_package_file_config_version}

${LCG_bjam_bin} ${LCG_boost_jam_opts} ${LCG_boost_compile_options} \
    --toolset=${LCG_boost_toolset} \
    --prefix=${LCG_destbindir} install 

mkdir ${LCG_destbindir}/data_files/
find ./ -name "*.csv" -exec cp {} ${LCG_destbindir}/data_files/ \;

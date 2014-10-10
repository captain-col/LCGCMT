#!/bin/sh

cd ${LCG_destbindir}/boost_${LCG_file_config_version}

${LCG_bjam_bin} ${LCG_boost_jam_opts} \
    ${LCG_boost_compile_options} \
    --toolset=${LCG_boost_toolset}

#!/bin/sh
date
cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
mkdir Python-${LCG_package_config_version}_shared
mkdir Python-${LCG_package_config_version}_static
mkdir Python-${LCG_package_config_version}_framework
${LCG_python_compile_options}

cd ${LCG_builddir}/Python-${LCG_package_config_version}_shared
${LCG_builddir}/Python-${LCG_package_config_version}/configure ${LCG_python_config_shared_options}

cd ${LCG_builddir}/Python-${LCG_package_config_version}_static
${LCG_builddir}/Python-${LCG_package_config_version}/configure ${LCG_python_config_static_options}

if [[ $CMTCONFIG == *mac* ]]; then
    cd ${LCG_builddir}/Python-${LCG_package_config_version}_framework
    ${LCG_builddir}/Python-${LCG_package_config_version}/configure ${LCG_python_config_framework_options}
fi

date

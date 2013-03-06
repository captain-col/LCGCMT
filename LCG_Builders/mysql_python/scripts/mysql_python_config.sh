#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
${LCG_mysql_python_compile_options}

if [ "$CMTCONFIG" == "x86_64-mac106-gcc42-opt" ] || [ "$CMTCONFIG" == "i386-mac106-gcc42-opt" ]; then 
cp ${LCG_extdir}/tarFiles/${LCG_tardiffname} ${LCG_builddir}/MySQL-python-${LCG_package_config_version}/
cd MySQL-python-${LCG_package_config_version}
patch -p0 <${LCG_tardiffname}

fi

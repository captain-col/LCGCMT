#!/bin/sh

cd ${LCG_builddir}/${LCG_package}${LCG_package_config_version}oss
mkdir -p ${LCG_destbindir}/bin
find ./ -name *release -exec rsync -azu {}/ ${LCG_destbindir}/bin \;
rsync -azu include ${LCG_destbindir}/
find ${LCG_destbindir} -name *sh  -exec sed -i 's%'"${LCG_builddir}/${LCG_package}${LCG_package_config_version}oss\""'%'"${LCG_destbindir}\""'%g' {} \;
find ${LCG_destbindir} -name *sh  -exec sed -i 's%'"${LCG_builddir}"'.*release%${TBBROOT}/bin%g' {} \;

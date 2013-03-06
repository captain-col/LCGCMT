#!/bin/sh

cd ${LCG_builddir}/gccxml-build
${LCG_gccxml_compile_options}
make install
cd ${LCG_destbindir}/share/gccxml-${LCG_gccxml_version_twodigit}
cp gccxml_config gccxml_config.org
sed s%COMPILER=\"/.*/%COMPILER=\"% gccxml_config > gccxml_config.2
mv gccxml_config.2 gccxml_config

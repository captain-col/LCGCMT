#!/bin/sh
date
cd ${LCG_builddir}/GAUDI/${LCG_package_config_version}/GaudiRelease/cmt

cmt show uses
cmt broadcast  -global -select="/${LCG_package_config_version}/"  cmt config

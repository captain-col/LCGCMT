#!/bin/sh

cd ${LCG_builddir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/src/config/cmt
. ./setup.sh ""
cmt broadcast -global -select="/${LCG_package_config_version}/" - cmt make

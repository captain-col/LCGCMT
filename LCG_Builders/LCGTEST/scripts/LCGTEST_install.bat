cd %LCG_builddir%/%LCG_pkgdest_pkgname%/%LCG_package_config_version%/src/config/cmt
set PWD=%LCG_builddir%/%LCG_pkgdest_pkgname%/%LCG_package_config_version%/src/config/cmt
set CMTPATH=
cmt broadcast rm -fr ../%LCG_CMTCONFIG%
cd ../../..
rsync -avz src include ${LCG_CMTCONFIG} ${LCG_reldir}/%LCG_pkgdest_pkgname%/${LCG_package_config_version}

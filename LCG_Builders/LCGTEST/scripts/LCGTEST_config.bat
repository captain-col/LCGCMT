cd /d %LCG_builddir%\%LCG_pkgdest_pkgname%\%LCG_package_config_version%\src\config\cmt
set PWD=%LCG_builddir%\%LCG_pkgdest_pkgname%\%LCG_package_config_version%\src\config\cmt
set CMTPATH=
cmt show uses
cmt broadcast  cmt config


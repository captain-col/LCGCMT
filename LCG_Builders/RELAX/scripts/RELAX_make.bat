cd %LCG_builddir%\RELAX\%LCG_package_config_version%\src\config\cmt
set PWD=%LCG_builddir%\RELAX\%LCG_package_config_version%\src\config\cmt
set CMTPATH=
cmt broadcast - nmake /f nmake all_groups

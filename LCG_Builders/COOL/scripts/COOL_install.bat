cd %LCG_builddir%\COOL\%LCG_package_config_version%\src\config\cmt
set PWD=%LCG_builddir%\COOL\%LCG_package_config_version%\src\config\cmt
set CMTPATH=
cmt broadcast rm -fr ..\%LCG_CMTCONFIG%
cd ..\..\..
md %LCG_CMTCONFIG% %LCG_reldir%\COOL\%LCG_package_config_version%\%LCG_CMTCONFIG%
xcopy %LCG_CMTCONFIG% %LCG_reldir%\COOL\%LCG_package_config_version%\%LCG_CMTCONFIG%  /E /C /H /Y

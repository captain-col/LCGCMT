cd %LCG_builddir%\CORAL\%LCG_package_config_version%\src\config\cmt
set PWD=%LCG_builddir%\CORAL\%LCG_package_config_version%\src\config\cmt
set CMTPATH=
cmt broadcast rm -fr ..\%LCG_CMTCONFIG%
cd ..\..\..
md %LCG_reldir%\CORAL\%LCG_package_config_version%\%LCG_CMTCONFIG%
xcopy %LCG_CMTCONFIG%  %LCG_reldir%\CORAL\%LCG_package_config_version%\%LCG_CMTCONFIG%   /E /C /H /Y

cd %LCG_builddir%\GAUDI\%LCG_package_config_version%\GaudiRelease\cmt
set PWD=%LCG_builddir%\GAUDI\%LCG_package_config_version%\GaudiRelease\cmt
set CMTPATH=

cmt broadcast rm -fr ..\%LCG_CMTCONFIG%
cd ..\..\InstallArea
set PWD=%LCG_builddir%\GAUDI\%LCG_package_config_version%
md %LCG_reldir%\GAUDI\%LCG_package_config_version%\InstallArea\%LCG_CMTCONFIG%
xcopy %LCG_CMTCONFIG% %LCG_reldir%\GAUDI\%LCG_package_config_version%\InstallArea\%LCG_CMTCONFIG% /E /C /H /Y

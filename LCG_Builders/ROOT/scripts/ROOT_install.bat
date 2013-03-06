set PATH=C:\cygwin\bin;%PATH%
cd %LCG_builddir%\ROOT\%LCG_CheckoutDir%
set PWD=%LCG_builddir%\ROOT\%LCG_CheckoutDir%
md %LCG_reldir%\ROOT\%LCG_package_config_version%\%LCG_CMTCONFIG%
xcopy  root %LCG_reldir%\ROOT\%LCG_package_config_version%\%LCG_CMTCONFIG%

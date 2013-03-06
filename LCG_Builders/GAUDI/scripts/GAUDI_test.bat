cd %LCG_builddir%\GAUDI\%LCG_package_config_version%\GaudiRelease\cmt
set PWD=%LCG_builddir%\GAUDI\%LCG_package_config_version%\GaudiRelease\cmt
set CMTPATH=

call setup.bat
cmt TestProject 
echo %DATE% > ..\..\..\logs\%CMTCONFIG%-qmtest.log
echo %TIME% >> ..\..\..\logs\%CMTCONFIG%-qmtest.log
cmt qmtest_summarize  >> ..\..\logs\%CMTCONFIG%-qmtest.log

cd %LCG_builddir%\LCGCMT\%LCG_package_config_version%\config\cmt
set PWD=%LCG_builddir%\LCGCMT\%LCG_package_config_version%\config\cmt

cmt config
call setup.bat

cd ..\qmtest
echo %DATE% > ..\..\logs\%CMTCONFIG%-qmtest.log
echo %TIME% >> ..\..\logs\%CMTCONFIG%-qmtest.log
qmtest run -o ..\..\logs\%CMTCONFIG%-qmtest-results.qmr >> ..\..\logs\%CMTCONFIG%-qmtest.log
qmtest summarize -f brief ..\..\logs\%CMTCONFIG%-qmtest-results.qmr >> ..\..\logs\%CMTCONFIG%-qmtest.log


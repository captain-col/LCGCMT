cd %LCG_builddir%\COOL\%LCG_package_config_version%\src\config\cmt
set PWD=%LCG_builddir%\COOL\%LCG_package_config_version%\src\config\cmt
set CMTPATH=

call  setup.bat
cd ..\qmtest
set PWD=%LCG_builddir%\COOL\%LCG_package_config_version%\src\config\qmtest
echo %DATE% > ..\..\..\logs\%CMTCONFIG%-qmtest.log
echo %TIME% >> ..\..\..\logs\%CMTCONFIG%-qmtest.log
qmtest run -o ..\..\..\logs\%CMTCONFIG%-qmtest-results.qmr %COOL_QMTEST_TARGET% >> ..\..\..\logs\%CMTCONFIG%-qmtest.log
qmtest summarize -f brief ..\..\..\logs\%CMTCONFIG%-qmtest-results.qmr >> ..\..\..\logs\%CMTCONFIG%-qmtest.log


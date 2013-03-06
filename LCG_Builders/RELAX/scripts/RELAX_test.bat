cd %LCG_builddir%\RELAX\%LCG_package_config_version%\src\config\cmt
set PWD=%LCG_builddir%\RELAX\%LCG_package_config_version%\src\config\cmt
set CMTPATH=

call setup.bat
cd ..\qmtest
echo %DATE% > ..\..\..\logs\%CMTCONFIG%-qmtest.log
echo %TIME% >> ..\..\..\logs\%CMTCONFIG%-qmtest.log
set PWD=%LCG_builddir%\RELAX\%LCG_package_config_version%\src\config\qmtest
qmtest run -o ..\..\..\logs\%CMTCONFIG%-qmtest-results.qmr >> ..\..\..\logs\%CMTCONFIG%-qmtest.log
qmtest summarize -f brief ..\..\..\logs\%CMTCONFIG%-qmtest-results.qmr >> ..\..\..\logs\%CMTCONFIG%-qmtest.log

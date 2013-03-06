cd %LCG_builddir%\CORAL\%LCG_package_config_version%\src\config\cmt
set PWD=%LCG_builddir%\CORAL\%LCG_package_config_version%\src\config\cmt
set CMTPATH=

call setup.bat
cd ..\qmtest

set PWD=%LCG_builddir%\CORAL\%LCG_package_config_version%\src\config\qmtest
echo %DATE% > ..\..\..\logs\%CMTCONFIG%-qmtest.log
echo %TIME%>> ..\..\..\logs\%CMTCONFIG%-qmtest.log
@echo off
setlocal ENABLEDELAYEDEXPANSION
set list=
for /f %%i in ('python createconfig.py') do set LIST=!LIST! %%i
echo %LIST%
call qmtest -D %LIST% run -o ..\..\..\logs\%CMTCONFIG%-qmtest-results.qmr >> ..\..\..\logs\%CMTCONFIG%-qmtest.log
qmtest summarize -f brief ..\..\..\logs\%CMTCONFIG%-qmtest-results.qmr >> ..\..\..\logs\%CMTCONFIG%-qmtest.log
endlocal


cd %LCG_builddir%\CORAL\%LCG_package_config_version%\src/config\cmt
set PWD=%LCG_builddir%\CORAL\%LCG_package_config_version%\src\config\cmt
set CMTPATH=
cmt broadcast - nmake /f nmake all_groups
call %CORAL_post_make_step%

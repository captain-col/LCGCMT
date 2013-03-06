
cd %LCG_builddir%\COOL\%LCG_package_config_version%\src\config\cmt
set PWD=%LCG_builddir%\COOL\%LCG_package_config_version%\src\config\cmt
set CMTPATH=
cmt broadcast - cmt make all_groups
call %COOL_post_make_step%

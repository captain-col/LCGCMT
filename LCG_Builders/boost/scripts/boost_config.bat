cd /D %LCG_builddir%
rem -- Assume that the tar file has already being expanded by 'cmt pkg_get' 
rem -- tar xvfj ${LCG_tarfilename}
cd /D %LCG_builddir%\boost_%LCG_package_file_config_version%
set ucfg=using python : %LCG_python_version_twodigit% : %LCG_python_root% ;
echo %ucfg% > user-config.jam
cd tools\build\v2
call ./bootstrap.bat


cd %LCG_builddir%\GAUDI\%LCG_package_config_version%\GaudiRelease\cmt
set PWD=%LCG_builddir%\GAUDI\%LCG_package_config_version%\GaudiRelease\cmt
set CMTPATH=
cmt show uses
cmt broadcast - cmt make all_groups

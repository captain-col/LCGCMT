cd %LCG_builddir%\GAUDIATLAS\%LCG_package_config_version%\GaudiRelease\cmt
set PWD=%LCG_builddir%\GAUDIATLAS\%LCG_package_config_version%\GaudiRelease\cmt
set CMTPATH=
cmt show uses
cmt broadcast - cmt make all_groups

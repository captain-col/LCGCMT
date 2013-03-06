#set echo on

set pythondir = `cmt -quiet show macro_value Python_home`
set pythonexe = ${pythondir}/bin/python


python ../python/lcg_InstallArea.py $*

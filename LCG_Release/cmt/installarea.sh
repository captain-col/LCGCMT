#set -x

pythondir=`cmt -quiet show macro_value Python_home`
pythonexe=${pythondir}/bin/python

${pythonexe} ../python/lcg_InstallArea.py $*

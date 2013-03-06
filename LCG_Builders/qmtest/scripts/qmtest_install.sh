#!/bin/sh

cd ${LCG_builddir}/qmtest-${LCG_package_config_version}
python setup.py install --prefix=${LCG_destbindir}


# Remove two places with hardcoded values in the installed files
cd ${LCG_destbindir}/bin
repl=`grep "/bin/python" qmtest`
mv qmtest qmtest.org
sed s%$repl%#!/usr/bin/env\ python% qmtest.org > qmtest

cd ${LCG_destbindir}/lib/python${LCG_python_config_version_twodigit}/site-packages/qm
repl=`grep prefix config.py`
rm config.pyc
mv config.py config.py.org
echo "import os" > config.py
sed s%$repl%prefix=os.path.realpath\(os.path.abspath\(os.path.dirname\(__file__\)\)+\(os.sep+os.pardir\)*4\)% config.py.org >> config.py
echo >> config.py

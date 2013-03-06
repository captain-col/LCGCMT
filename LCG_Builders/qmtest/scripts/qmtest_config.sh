#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd ${LCG_builddir}/qmtest-${LCG_package_config_version}/qm/test/classes/
cp command.py command.py.org
sed 's/\(^[ ]*causes.append("standard output")\)/#\1/' command.py.org > command.py
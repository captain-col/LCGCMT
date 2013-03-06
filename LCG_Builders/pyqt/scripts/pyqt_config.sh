#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd PyQt-${LCG_pyqt_plat_name}-gpl-${LCG_package_config_version}
PyQt_extdir=${LCG_destdir}/${LCG_CMTCONFIG}
python configure.py -b ${PyQt_extdir}/bin -d ${PyQt_extdir}/lib/python${LCG_python_version_twodigit}/site-packages/ -l ${LCG_python_home}/include/python${LCG_python_version_twodigit} -m ${LCG_python_home}/lib/python${LCG_python_version_twodigit}/config -q ${LCG_qt_home}/bin/qmake -v ${PyQt_extdir}/share/sip/PyQt4 -p ${PyQt_extdir}/plugins --verbose --confirm-license

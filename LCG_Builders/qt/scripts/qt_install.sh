#!/bin/sh

cd ${LCG_builddir}/${LCG_qt_pkgname}
make install_subtargets
make install_translations 
make install_qmake 
make install_mkspecs


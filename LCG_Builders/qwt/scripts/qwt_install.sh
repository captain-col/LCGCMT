#!/bin/sh

cd ${LCG_builddir}/qwt-${LCG_package_config_version}

#Pick out a few sub-targets to avoid attempts to install designer plugin in qt directory.
#Also, remove the doc/ dir afterwards to save on space.
make sub-src-install_subtargets sub-textengines-install_subtargets && rm -rf ${LCG_destbindir}/doc

#Copy over the designer plugin by hand:
PLUGFILE=${LCG_builddir}/qwt-${LCG_package_config_version}/designer/plugins/designer/${LCG_qwt_designerplugfile}
PLUGFILE_TARGETDIR=${LCG_destbindir}/plugins/designer
mkdir -p ${PLUGFILE_TARGETDIR}
install -m 644 -p $PLUGFILE $PLUGFILE_TARGETDIR/${LCG_qwt_designerplugfile}

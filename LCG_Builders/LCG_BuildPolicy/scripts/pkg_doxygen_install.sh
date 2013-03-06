#!/bin/sh

doxy_destdir=`dirname ${LCG_PKG_DEST_DIR}`

rsync -avz ${LCG_DOXY_WORK_DIR}/../../doc ${doxy_destdir}/

cd ${doxy_destdir}/doc/doxygen/html
ln -s reference_tags.xml ${LCG_package}_reference_tags.xml
ln -s reference_tags.xml ${LCG_package_config_version}_reference_tags.xml

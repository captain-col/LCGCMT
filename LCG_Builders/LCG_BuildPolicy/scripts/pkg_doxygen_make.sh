#!/bin/sh

mkdir -p ${LCG_DOXY_WORK_DIR}
mkdir -p ${LCG_DOXY_CFG_DIR}

cd ${LCG_DOXY_CFG_DIR}
cp ${LCG_BUILDPOLICYROOT_DIR}/doc/doxygen/* .
cp ${LCG_package_root}/doc/doxygen/* .

doxygen ./Doxyfile_${LCG_package}.cfg
python ${LCG_BUILDPOLICYROOT_DIR}/scripts/repl_string.py ${LCG_DOXY_WORK_DIR}/html/reference_tags.xml ${LCG_PKG_SRC_DIR} ${LCG_PKG_DEST_DIR}

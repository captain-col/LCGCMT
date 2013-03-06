
#!/bin/sh

# used to process 
# . ${LCG_BUILDPOLICYROOT_DIR}/scripts/pkg_doxygen_make.sh
# now we change doxygen file on the fly 

mkdir -p ${LCG_DOXY_WORK_DIR}
mkdir -p ${LCG_DOXY_CFG_DIR}

cd ${LCG_DOXY_CFG_DIR}
cp ${LCG_BUILDPOLICYROOT_DIR}/doc/doxygen/* .
cp ${LCG_package_root}/doc/doxygen/* .

sed s/PROJECT_NUMBER/PROJECT_NUMBER=${LCG_clhep_config_version}\ \#/ Doxyfile_clhep.cfg > Doxyfile_clhep.cfg.2
mv Doxyfile_clhep.cfg.2 Doxyfile_clhep.cfg
sed s/VERSION/${LCG_clhep_config_version}/ clhep_doxygen.template > clhep_doxygen.template.3
mv clhep_doxygen.template.3 clhep_doxygen.template

doxygen ./Doxyfile_${LCG_package}.cfg
python ${LCG_BUILDPOLICYROOT_DIR}/scripts/repl_string.py ${LCG_DOXY_WORK_DIR}/html/reference_tags.xml ${LCG_PKG_SRC_DIR} ${LCG_PKG_DEST_DIR}


#/bin/sh

cd ${LCG_builddir}/${LCG_package}/${LCG_package_config_version}/${CMTBIN}
rm -fr *.o *.make cmt_deps
cd ..
rsync -avz . ${LCG_destdir}
cd ${LCG_destdir}/mgr
./INSTALL

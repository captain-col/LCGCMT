#!/bin/sh

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}-obj
make install

LCG_gcc_vers=`echo ${LCG_package_config_version} | cut -c 1,3`
cd ${LCG_destbindir}/bin 
ln -s g++ g++${LCG_gcc_vers}
ln -s c++ c++${LCG_gcc_vers}
ln -s gcc gcc${LCG_gcc_vers}
ln -s gfortran gfortran${LCG_gcc_vers}
ln -s g++ lcg-g++-${LCG_package_config_version}
ln -s c++ lcg-c++-${LCG_package_config_version}
ln -s gcc lcg-gcc-${LCG_package_config_version}
ln -s gfortran lcg-gfortran-${LCG_package_config_version}

cd ${LCG_destbindir}/${LCG_libdirname}
rsync -avz ${LCG_mpfr_home}/lib/libmpfr* .
rsync -avz ${LCG_gmp_home}/lib/libgmp* .
rsync -avz ${LCG_mpc_home}/lib/libmpc* .
rsync -avz ${LCG_libelf_home}/lib/libelf* .
rsync -avz ${LCG_ppl_home}/lib/libp* .
rsync -avz ${LCG_cloog_home}/lib/libcloog* .
for f in `find . -type f -name "*.so*"`; do strip $f; done

if [ x`uname -p` = xx86_64 ] ; then
   LCG_mpfr32_home=`echo ${LCG_mpfr_home} | ${LCG_sed_chg_cmtconfig}` ;\
   LCG_gmp32_home=`echo ${LCG_gmp_home} | ${LCG_sed_chg_cmtconfig}` ;\
   LCG_mpc32_home=`echo ${LCG_mpc_home} | ${LCG_sed_chg_cmtconfig}` ;\
   LCG_libelf32_home=`echo ${LCG_libelf_home} | ${LCG_sed_chg_cmtconfig}` ;\
   LCG_ppl32_home=`echo ${LCG_ppl_home} | ${LCG_sed_chg_cmtconfig}` ;\
   LCG_cloog32_home=`echo ${LCG_cloog_home} | ${LCG_sed_chg_cmtconfig}` ;\
   cd ${LCG_destbindir}/lib ;\
   rsync -avz ${LCG_mpfr32_home}/lib/libmpfr* . ;\
   rsync -avz ${LCG_gmp32_home}/lib/libgmp* . ;\
   rsync -avz ${LCG_mpc32_home}/lib/libmpc* . ;\
   rsync -avz ${LCG_libelf32_home}/lib/libelf* . ;\
   rsync -avz ${LCG_ppl32_home}/lib/libp* . ;\
   rsync -avz ${LCG_cloog32_home}/lib/libcloog* . ;\
   for f in `find . -type f -name "*.so*"`; do strip $f; done ;\
fi



#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
tar xvfz ${LCG_tardiffname}

ln -s ${gcc_link}/gcc cc
export PATH=`pwd`:$PATH
echo $PATH

cd e2fsprogs-${LCG_package_config_version}
chmod 744 lib/Makefile.elf-lib

#patch -p0 < ../uuid1.38p1.diff
${LCG_uuid_compile_options}
./configure --prefix=${LCG_extdir}/uuid/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_uuid_config_options}
cd ../
chmod 744  e2fsprogs-${LCG_package_config_version}/lib/*/Makefile
patch -p0 < blkid.Makefile.diff
patch -p0 < et.Makefile.diff
patch -p0 < e2p.Makefile.diff
patch -p0 < ext2fs.Makefile.diff
patch -p0 < ss.Makefile.diff
patch -p0 < uuid.Makefile.diff

#!/bin/sh

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}

## output dir
mkdir lib

## create a custom makefile (for the static build)
cat >| make.inc << EOF
SHELL = /bin/sh
PLAT =
FORTRAN  = ${LCG_lapack_for}
OPTS     = ${LCG_lapack_static_opts}
DRVOPTS  = ${LCG_lapack_static_opts}
NOOPT    = ${LCG_lapack_static_noopt}
LOADER   = ${LCG_lapack_for}
LOADOPTS = 

TIMER = INT_ETIME

ARCH      = ar
ARCHFLAGS = ${LCG_lapack_static_archflags}
RANLIB    = ranlib

BLASLIB   = ${LCG_lapack_static_blaslib}
LAPACKLIB = ${LCG_lapack_static_lib}
TMGLIB    = tmglib.a
EIGSRCLIB = eigsrc.a
LINSRCLIB = linsrc.a
EOF

## make the static build
make lapacklib
cp *.a lib/.

make clean

## create a custom makefile (for the shared build)
cat >| make.inc << EOF
SHELL = /bin/sh
PLAT =
FORTRAN  = ${LCG_lapack_for}
OPTS     = ${LCG_lapack_opts}
DRVOPTS  = ${LCG_lapack_opts}
NOOPT    = ${LCG_lapack_noopt}
LOADER   = ${LCG_lapack_for}
LOADOPTS = 

TIMER = INT_ETIME

ARCH      = ${LCG_lapack_for}
ARCHFLAGS = ${LCG_lapack_archflags}
RANLIB    = echo

BLASLIB   = ${LCG_lapack_blaslib}
LAPACKLIB = ${LCG_lapack_lib}
TMGLIB    = libtmglib.so.3
EIGSRCLIB = libeigsrc.so.3
LINSRCLIB = liblinsrc.so.3
EOF

## make the shared build
make lapacklib
cp *.so lib/.
cd lib
ln -s libLAPACK.a liblapack3.a ; ln -s libLAPACK.so liblapack3.so
if [[ $CMTCONFIG == *slc* ]]; then
    ln -s libLAPACK.so liblapack.so
    ln -s libLAPACK.a liblapack.a
fi

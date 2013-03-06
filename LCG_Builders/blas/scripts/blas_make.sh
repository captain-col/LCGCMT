#!/bin/sh

cd ${LCG_builddir}/BLAS

mkdir ${LCG_builddir}/BLAS/arch
cd ${LCG_builddir}/BLAS/arch
ln -s ../*.f ../Makefile ../make.inc .
make FORTRAN=${LCG_BLAS_FORTRAN} OPTS="${LCG_BLAS_SHCOPTS}" BLASLIB=libBLAS.a
# MAC is case insensitive
if [[ $CMTCONFIG == *slc* ]]; then
    ln -s libBLAS.a libblas.a
fi


mkdir ${LCG_builddir}/BLAS/shlib
cd ${LCG_builddir}/BLAS/shlib
ln -s ../*.f ../Makefile ../make.inc .
make FORTRAN=${LCG_BLAS_FORTRAN} OPTS="${LCG_BLAS_SHCOPTS}" ARCH=${LCG_BLAS_FORTRAN} ARCHFLAGS="${LCG_BLAS_SHLIBFLAGS}" BLASLIB=libBLAS.so RANLIB=echo
# MAC is case insensitive
if [[ $CMTCONFIG == *slc* ]]; then
    ln -s libBLAS.so libblas.so
fi

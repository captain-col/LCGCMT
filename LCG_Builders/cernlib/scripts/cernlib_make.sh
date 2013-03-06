#!/bin/sh

export CERN_LEVEL=${LCG_CERN_LEVEL}
export CERN=${LCG_builddir}/cernlib
export CERN_ROOT=${CERN}/${CERN_LEVEL}
export CVSCOSRC=${CERN_ROOT}/src
export PATH=${CERN_ROOT}/bin:$PATH

echo $CERN_LEVEL
echo $CERN
echo $CERN_ROOT
echo $CVSCOSRC
echo $PATH

cd $CERN_ROOT
mkdir -p build/log bin lib

cd $CERN_ROOT/build
$CVSCOSRC/config/imake_boot 

gmake bin/kuipc
gmake scripts/Makefile

cp ${LCG_BLAS_HOME}/lib/libBLAS.a ${CERN_ROOT}/lib/libblas.a
cp ${LCG_LAPACK_HOME}/lib/liblapack3.a ${CERN_ROOT}/lib/liblapack3.a

cd $CERN_ROOT/build/scripts
gmake install.bin
gmake bin/cernlib

if [ x${LCG_PATCH_BIN_CERNLIB} == xYES -a ! -f $CERN_ROOT/bin/cernlib.org ] ; then \
cp $CERN_ROOT/bin/cernlib $CERN_ROOT/bin/cernlib.org ; \
sed s%/usr/X11R6/lib%/usr/X11R6/lib64%g $CERN_ROOT/bin/cernlib.org > $CERN_ROOT/bin/cernlib ; \
fi
chmod a+rx $CERN_ROOT/bin/*

cd $CERN_ROOT/build
gmake

cd $CERN_ROOT/build/scripts
gmake install.bin

cd $CERN_ROOT/build/pawlib
gmake install.bin

cd $CERN_ROOT/build/packlib
gmake install.bin

cd $CERN_ROOT/build/patchy
gmake

# Fix data file
cd $CERN_ROOT/lib
rm xsneut95.dat 
ln -s ../src/geant321/data/xsneut95.dat .

# nypatchy et al
cd $CERN_ROOT/build
gmake patchy/Makefile
cd patchy
cp Makefile Makefile.org
sed s/fcasplit\ p5lib.f/fcasplit\ -f\ $LCG_FOR\ p5lib.f/ Makefile.org > Makefile
mkdir p5boot
cd p5boot/
$LCG_FOR -c $CERN_ROOT/src/p5boot/p5lib/*.f
ar cr libp5.a *.o
$LCG_FOR -o nypatchy $CERN_ROOT/src/p5boot/nypatchy.f libp5.a $CERN_ROOT/lib/libkernlib.a 
cp nypatchy $CERN_ROOT/bin/
cd $CERN_ROOT/bin
ln -s nypatchy ypatchy
cd $CERN_ROOT/build/patchy
make install.bin


# make noshift libs links
cd $CERN_ROOT/lib
mv libpacklib.a libpacklib_noshift.a
ln -s libpacklib_noshift.a libpacklib.a
mv libkernlib.a libkernlib_noshift.a
ln -s libkernlib_noshift.a libkernlib.a
cd $CERN_ROOT/bin
cp cernlib cernlib_noshift

# make all in bin executable 
chmod a+rx $CERN_ROOT/bin/*


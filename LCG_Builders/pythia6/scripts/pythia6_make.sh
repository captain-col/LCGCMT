#!/bin/sh

cd ${LCG_destbindir}

# The fortran source for pythia
pythia_src=${LCG_tardir}/pythia-${LCG_package_config_version}.f.gz

# The tar file with the ROOT interface.
pythia_tar=${LCG_tardir}/pythia6.tar.gz

# A utility needed to build the source.
fsplit_src=${LCG_package_root}/scripts/fsplit.c

############################################################################
#
# pick a fortran:  g77 vs. gfortran vs. g95
#
whichftn="unknown"
whichgfortran=`which gfortran | grep -v "no gfortran in"`
if [ ! -z "${whichgfortran}" ] ; then 
    whichftn="gfortran"
else
    #      echo "no gfortran"
    whichg77=`which g77 | grep -v "no g77 in"`
    if [ ! -z "${whichg77}" ] ; then 
        whichftn="g77"
    else
        echo "could not find a fortran compiler (gfortran or g77)"
    fi
fi
export FORT=$whichftn
echo "using $FORT as fortran compiler"

#########################################################################
# Setup the directories
cd ${LCG_destbindir}
for subdir in inc lib src tpythia6_build ; do
    rm -rf ${subdir}
    mkdir ${subdir}
done

#########################################################################
# Build the fsplit utility
cd ${LCG_destbindir}/src
gcc -ansi -o fsplit ${fsplit_src}

########################################################################
# Build the split fortran source
zcat ${pythia_src} | ./fsplit
rm zzz*.f

############################################################################
#
# create a Makefile for the pythia6 source code and then use it to compile.
#
cd ${toppath}/src
cat > Makefile <<EOF
#
# simple pythia6 makefile
#
UNAME = \$(shell uname)
ifeq "\$(UNAME)" "Linux"
    AR=ar
    F77=$FORT
    FFLAG= -O -fno-second-underscore -fPIC $m32flag
    CPP = gcc -E 
    CPPFLG= -C -P
endif
ifeq "\$(UNAME)" "Darwin"
    AR=ar
    F77=$FORT
    FFLAG= -O -fno-second-underscore -fPIC $m32flag
    CPP = cc -E
    CPPFLG= -C -P
endif
LIB = ../lib
CPPFLGS = \$(CPPFLG) -D\$(UNAME)

FOBJSALL = \$(patsubst %.f,%.o,\$(wildcard *.f)) \
           \$(patsubst %.F,%.o,\$(wildcard *.F))

# remove the "pdfdum.o" as we don't want that going into the .a library
FOBJS = \$(filter-out pdfdum.o,\$(FOBJSALL))

#------------------------------------------

all: \$(LIB)/liblund.a \$(LIB)/pydata.o 

\$(LIB)/liblund.a: \$(FOBJS) 
	\$(AR) -urs \$(LIB)/liblund.a \$(FOBJS) 

\$(LIB)/pydata.o: pydata.o
	cp -p pydata.o \$(LIB)/pydata.o

\$(LIB)/pdfdum.o: pdfdum.o
	cp -p pdfdum.o \$(LIB)/pdfdum.o

clean:
	rm -f *.o

veryclean:
	rm -f \$(LIB)/liblund.a \$(LIB)/pydata.o \$(LIB)/pdfdum.o
	rm -f *.o

#------------------------------------------

.SUFFIXES : .o .f .F

.f.o:
	\$(F77) \$(FFLAG) -c \$<

.F.o: 
	\$(F77) \$(FFLAG) -c \$<

EOF
make all

############################################################################
#
# build the ROOT interface library libPythia6.so 
#
echo "build ROOT accessable shared library"
cd ${LCG_destbindir}/tpythia6_build

tar xzvf ${toppath}/download/pythia6.tar.gz pythia6/tpythia6_called_from_cc.F
tar xzvf ${toppath}/download/pythia6.tar.gz pythia6/pythia6_common_address.c
mv pythia6/* .
rmdir pythia6
echo 'void MAIN__() {}' > main.c
gcc -c -fPIC $m32flag main.c
gcc -c -fPIC $m32flag pythia6_common_address.c
$FORT -c -fPIC -fno-second-underscore $m32flag tpythia6_called_from_cc.F

cd ${LCG_destbindir}/lib

arch=`uname`
if [ ${arch} = "Linux" ] ; then
  $FORT $m32flag -shared -Wl,-soname,libPythia6.so -o libPythia6.so \
    ${LCG_destbindir}/tpythia6_build/*.o ${LCG_destbindir}/src/*.o ${CERNLINK}
fi
if [ ${arch} = "Darwin" ] ; then
  macosx_minor=`sw_vers | sed -n 's/ProductVersion://p' | cut -d . -f 2`
  gcc $m32flag -dynamiclib -flat_namespace -single_module -undefined dynamic_lookup \
      -install_name ${LCG_destbindir}/lib/libPythia6.dylib -o libPythia6.dylib \
      ${LCG_destbindir}/tpythia6_build/*.o ${LCG_destbindir}/src/*.o ${CERNLINK}
  if [ $macosx_minor -ge 4 ]; then
     ln -sf libPythia6.dylib libPythia6.so
  else
     gcc $m32flag -bundle -flat_namespace -undefined dynamic_lookup -o libPythia6.so \
      ${LCG_destbindir}/tpythia6_build/*.o ${LCG_destbindir}/src/*.o ${CERNLINK}
  fi
fi

############################################################################
#
# create pythia6 include files for common blocks
#
# here we'd like to automate the extraction of the common common blocks
# into include files but it's non-trivial

echo "extract include files"
cd ${LCG_destbindir}/inc

# define a #include that declares the types of all the pythia functions
cat > pyfunc.inc <<EOF
C...standard pythia functions
      double precision PYFCMP,PYPCMP
      double precision PYCTEQ,PYGRVV,PYGRVW,PYGRVS,PYCT5L,PYCT5M,PYHFTH
      double precision PYGAMM,PYSPEN,PYTBHS,PYRNMQ,PYRNM3,PYFINT,PYFISB
      double precision PYXXZ6,PYXXGA,PYX2XG,PYX2XH,PYH2XX
      double precision PYGAUS,PYGAU2,PYSIMP,PYLAMF,PYTHAG
      double precision PYRVSB,PYRVI1,PYRVI2,PYRVI3,PYRVG1,PYRVG2,PYRVG3
      double precision PYRVG4,PYRVR, PYRVS, PY4JTW,PYMAEL
      double precision PYMASS,PYMRUN,PYALEM,PYALPS,PYANGL
      double precision PYR,   PYP
      integer          PYK,PYCHGE,PYCOMP
      character*40     VISAJE

      external         PYFCMP,PYPCMP
      external         PYCTEQ,PYGRVV,PYGRVW,PYGRVS,PYCT5L,PYCT5M,PYHFTH
      external         PYGAMM,PYSPEN,PYTBHS,PYRNMQ,PYRNM3,PYFINT,PYFISB
      external         PYXXZ6,PYXXGA,PYX2XG,PYX2XH,PYH2XX
      external         PYGAUS,PYGAU2,PYSIMP,PYLAMF,PYTHAG
      external         PYRVSB,PYRVI1,PYRVI2,PYRVI3,PYRVG1,PYRVG2,PYRVG3
      external         PYRVG4,PYRVR, PYRVS, PY4JTW,PYMAEL
      external         PYMASS,PYMRUN,PYALEM,PYALPS,PYANGL
      external         PYR,   PYP
      external         PYK,PYCHGE,PYCOMP
      external         VISAJE
EOF

# how to "automate" the others ... including declaring the types
# without using the IMPLICIT DOUBLE PRECISION etc.
# NEUGEN3 needs pydat1.inc pydat3.inc pyjets.inc at a minimum
# !!!! for now just hard-code them !!!

cat > pydat1.inc <<EOF
C...Parameters.
      integer       MSTU,               MSTJ
      double precision        PARU,               PARJ
      COMMON/PYDAT1/MSTU(200),PARU(200),MSTJ(200),PARJ(200)
EOF

cat > pydat2.inc <<EOF
C...Particle properties + some flavour parameters.
      integer       KCHG
      double precision          PMAS,       PARF,      VCKM
      COMMON/PYDAT2/KCHG(500,4),PMAS(500,4),PARF(2000),VCKM(4,4)
EOF

cat > pydat3.inc <<EOF
C...Decay information
      integer       MDCY,       MDME,                   KFDP
      double precision                       BRAT
      COMMON/PYDAT3/MDCY(500,3),MDME(8000,2),BRAT(8000),KFDP(8000,5)
EOF

cat > pyjets.inc <<EOF
C...The event record.
      integer       N,NPAD,K
      double precision               P,        V
      COMMON/PYJETS/N,NPAD,K(4000,5),P(4000,5),V(4000,5)
      SAVE  /PYJETS/
EOF

cat > pypars.inc <<EOF
C...Parameters.
      integer       MSTP,               MSTI
      double precision        PARP,               PARI
      COMMON/PYPARS/MSTP(200),PARP(200),MSTI(200),PARI(200)
EOF

cat > pysubs.inc <<EOF
C...Selection of hard scattering subprocesses
      integer       MSEL,MSELPD,MSUB,     KFIN
      double precision                                   CKIN
      COMMON/PYSUBS/MSEL,MSELPD,MSUB(500),KFIN(2,-40:40),CKIN(200)
EOF

############################################################################
#
# done
#
echo "end-of-script $0"
# End-of-Script

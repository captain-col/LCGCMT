#!/bin/sh

cd ${LCG_builddir}/root
mkdir -p ${LCG_destbindir}/lib
rsync -avz lib/libMathCore.* lib/libMathMore.* lib/libMinuit2.* lib/libSmatrix.* ${LCG_destbindir}/lib
mkdir -p ${LCG_destbindir}/include
rsync -avz --exclude "*LinkDef*" math/mathcore/inc/* math/mathmore/inc/* math/minuit2/inc/* math/smatrix/inc/* ${LCG_destbindir}/include
#rsync -avz roofit/doc ${LCG_destbindir}/

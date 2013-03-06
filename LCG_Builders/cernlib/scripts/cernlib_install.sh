#!/bin/sh

mkdir -p ${LCG_destbindir}
cd ${LCG_builddir}/cernlib/${LCG_CERN_LEVEL}
if [ ! -d ${LCG_destdir}/src ] ; then rsync -avz src include ${LCG_destdir} ; fi
rsync -avz bin lib ${LCG_destbindir}
cd ${LCG_destbindir} 
ln -s ../src .
ln -s ../include .

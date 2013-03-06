#!/bin/sh

cd ${LCG_builddir}/aida
mkdir -p ${LCG_destbindir}
rsync -avz * ${LCG_destbindir}

#!/bin/sh

cd ${LCG_builddir}/root
make all-mathcore all-mathmore all-minuit2 all-smatrix -j12


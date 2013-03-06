#!/bin/sh
date
cd ${LCG_builddir}
if [ -f  ./${LCG_tarfilename} ]; then 
    if [ ! -d $LCG_package]; then
        mkdir $LCG_package
    fi
    cd $LCG_package
	tar xvfz ../${LCG_tarfilename}
fi


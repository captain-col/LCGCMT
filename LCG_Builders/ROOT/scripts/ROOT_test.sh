#!/bin/sh
if [ x$LCG_IsCernVM == "xyes" ]; then
	date > $LCG_CernVMSumfile
else
	date
fi	

export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=.:$DYLD_LIBRARY_PATH
export PATH=$ROOTSYS/bin:$PATH
cd ${LCG_builddir}/ROOT/${LCG_CheckoutDir}/roottest

unset CXXFLAGS

if [ x$LCG_IsCernVM == "xyes" ]; then
	make -k >> $LCG_CernVMSumfile
        date >> $LCG_CernVMSumfile
else
        make -k
	date
fi 

# code coverage

if [[ ! -z "$GCOV_TOOL" ]];then 
	echo starting code coverage for ROOT
	bash ${LCG_BUILDPOLICYROOT_DIR}/scripts/pkg_coverage.sh 
fi


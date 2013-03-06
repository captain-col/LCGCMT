#!/bin/sh

cd ${LCG_builddir}/RELAX/${LCG_package_config_version}/src/config/cmt
if [[ ! -d ${LCG_builddir}/RELAX/${LCG_package_config_version}/logs ]]
then 
	echo "logs directory in RELAX project does not exists..creating." 
	mkdir ${LCG_builddir}/RELAX/${LCG_package_config_version}/logs
fi

. ./setup.sh
cd ../qmtest

LOGFILE=../../../logs/$CMTCONFIG-qmtest.log
SUMFILE=../../../logs/$CMTCONFIG-qmtest-results.qmr
if [ x$LCG_IsCernVM == "xyes" ]; then
  LOGFILE=$LCG_CernVMLogfile
  SUMFILE=$LCG_CernVMSumfile
fi

date > $LOGFILE
qmtest run -o $SUMFILE >> $LOGFILE
qmtest summarize -f brief $SUMFILE >> $LOGFILE
date >> $LOGFILE

# code coverage
cmt show macro gcov_linkopts 
[[ $? -eq 0 ]] && bash ${LCG_BUILDPOLICYROOT_DIR}/scripts/pkg_coverage.sh 2>&1

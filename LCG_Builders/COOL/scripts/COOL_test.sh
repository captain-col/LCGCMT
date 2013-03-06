#!/bin/sh

cd ${LCG_builddir}/COOL/${LCG_package_config_version}/src/config/cmt
if [[ ! -d ${LCG_builddir}/COOL/${LCG_package_config_version}/logs ]]
then 
	echo "logs directory in COOL project does not exists..creating." 
	mkdir ${LCG_builddir}/COOL/${LCG_package_config_version}/logs
fi
cmt config
. ./setup.sh
cd ../qmtest

LOGFILE=../../../logs/$CMTCONFIG-qmtest.log
SUMFILE=../../../logs/$CMTCONFIG-qmtest-results.qmr
if [ x$LCG_IsCernVM == "xyes" ]; then
  LOGFILE=$LCG_CernVMLogfile
  SUMFILE=$LCG_CernVMSumfile
fi

if [ "$IGPROF_REF_RES" != "" ] ; then
   mkdir -p $IGPROF_TEST_RES/raw/mem/
   mkdir -p $IGPROF_TEST_RES/raw/perf
   mkdir -p $IGPROF_TEST_RES/res/total
   mkdir -p $IGPROF_TEST_RES/res/live
   mkdir -p $IGPROF_TEST_RES/res/perf
   cd ..
   cp -r qmtest qmtest.igprof 
   cd qmtest.igprof 
   export PATH=$PATH:${LCG_BUILDPOLICYROOT_DIR}/scripts
   sedIgprof.sh "${LCG_builddir}/COOL/${LCG_package_config_version}/src/config/qmtest.igprof"
fi

date > $LOGFILE
qmtest run -o $SUMFILE ${COOL_QMTEST_TARGET} >> $LOGFILE
qmtest summarize -f brief $SUMFILE >> $LOGFILE
date >> $LOGFILE

if [ "$IGPROF_REF_RES" != "" ] ; then
   generateIgprof.py $LOGFILE
fi

# code coverage
cmt show macro gcov_linkopts 
[[ $? -eq 0 ]] && bash ${LCG_BUILDPOLICYROOT_DIR}/scripts/pkg_coverage.sh 2>&1 ../../../logs/$CMTCONFIG-coverage.log


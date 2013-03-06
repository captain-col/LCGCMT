#!/bin/sh

cd ${LCG_builddir}/LCGCMT/${LCG_package_config_version}/config/cmt
cmt config
source  setup.sh
cd ../qmtest

LOGFILE=../../logs/$CMTCONFIG-qmtest.log
SUMFILE=../../logs/$CMTCONFIG-qmtest-results.qmr
if [ x$LCG_IsCernVM == "xyes" ]; then
  LOGFILE=$LCG_CernVMLogfile
  SUMFILE=$LCG_CernVMSumfile
fi

date > $LOGFILE
qmtest run -o $SUMFILE >> $LOGFILE
qmtest summarize -f brief $SUMFILE >> $LOGFILE
date >> $LOGFILE

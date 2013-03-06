#!/bin/sh

echo " "
echo "=========================="
echo " testing using cmake build"
echo "=========================="
echo " " 

cd $G4WORKDIR

G4QMTESTDIR=${G4INSTALL}/tests/tools/qmtest

# set environment using cmake provided script
. geant4make.sh

export XERCESCROOT=$VARXERCESCROOT

export G4LIB_BUILD_GDML=1

echo $G4INSTALL

#export QMTESTSUITE="testall"

export WEEKDAY=`date +%a`
if [ "$WEEKDAY" = "$G4TEST_LARGE_N" ] ; then
   export QMTESTSUITE="testall-large_n"
fi

cd ${G4QMTESTDIR}

date > ../../../logs/$CMTCONFIG-qmtest.log
hostname >> ../../../logs/$CMTCONFIG-qmtest.log

[ ! -d $G4WORKDIR/tmp/$G4SYSTEM ] && mkdir -p $G4WORKDIR/tmp/$G4SYSTEM
[ ! -d $G4WORKDIR/bin/$G4SYSTEM ] && mkdir -p $G4WORKDIR/bin/$G4SYSTEM

${QMTESTEXE} run -j 2 -o ../../../logs/$CMTCONFIG-qmtest-results.qmr $QMTESTSUITE >> ../../../logs/$CMTCONFIG-qmtest.log
${QMTESTEXE} summarize -f brief ../../../logs/$CMTCONFIG-qmtest-results.qmr >> ../../../logs/$CMTCONFIG-qmtest.log

# would be nice to have only ... but parsing does not like this...
#${QMTESTEXE} run -j 2 -f brief -o ../../../logs/$CMTCONFIG-qmtest-results.qmr $QMTESTSUITE >> ../../../logs/$CMTCONFIG-qmtest.log

# brief log file -- not needed any more
#cat  ../../../logs/$CMTCONFIG-qmtest.log | tr $SEP "@@@" | awk -F "TESTS THAT DID " '{ print $3 }'| tr "@@@" $SEP >> ../../../../../www/${LCG_NGT_SLT_NAME}.${WEEKDAY}_${LCG_package_config_version}-$CMTCONFIG-qmtest.brief.log

date >> ../../../logs/$CMTCONFIG-qmtest.log



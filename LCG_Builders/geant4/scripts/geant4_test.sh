#!/bin/sh

if test $LCG_NGT_SLT_NAME == "g4tags" ; then
  
   /bin/sh $LCG_package_root/scripts/geant4_cmake_test.sh  $*

else

   export XERCESCROOT=$VARXERCESCROOT
   echo $G4INSTALL

#   export QMTESTSUITE="testall"

   export WEEKDAY=`date +%a`
   if [ "$WEEKDAY" = "$G4TEST_LARGE_N" ] ; then
      export QMTESTSUITE="testall-large_n"
   fi

   cd ${G4INSTALL}/tests/tools/qmtest

   date > ../../../logs/$CMTCONFIG-qmtest.log
   hostname >> ../../../logs/$CMTCONFIG-qmtest.log

#   filter out tests using root when ROOTSYS is not set
   if [ "${ROOTSYS:-no}" = "no" ] ; then
      mv $QMTESTSUITE.qms $QMTESTSUITE.tmp
      sed -e'/_using_ROOT/d' $QMTESTSUITE.tmp > $QMTESTSUITE.qms
   fi
   
[ ! -d $G4WORKDIR/tmp/$G4SYSTEM ] && mkdir -p $G4WORKDIR/tmp/$G4SYSTEM
[ ! -d $G4WORKDIR/bin/$G4SYSTEM ] && mkdir -p $G4WORKDIR/bin/$G4SYSTEM

opt_j=4

[ "X_$G4SYSTEM" = "X_WIN32_VC" ] && opt_j=2

if [ "X_$G4SYSTEM" = "X_Linux-g++" ] ; then
  number_cpu=`cat /proc/cpuinfo | grep ^processor | wc -l`
  [ $number_cpu -lt $opt_j ] &&  opt_j=$number_cpu
fi  
echo ".. parallel running of tests using -j $opt_j">> ../../../logs/$CMTCONFIG-qmtest.log 

   ${QMTESTEXE} run -j $opt_j -o ../../../logs/$CMTCONFIG-qmtest-results.qmr $QMTESTSUITE >> ../../../logs/$CMTCONFIG-qmtest.log
   ${QMTESTEXE} summarize -f brief ../../../logs/$CMTCONFIG-qmtest-results.qmr >> ../../../logs/$CMTCONFIG-qmtest.log

   # would be nice to have only ... but parsing does not like this...
   #${QMTESTEXE} run -j 2 -f brief -o ../../../logs/$CMTCONFIG-qmtest-results.qmr $QMTESTSUITE >> ../../../logs/$CMTCONFIG-qmtest.log

   # brief log file -- not needed any more
   #cat  ../../../logs/$CMTCONFIG-qmtest.log | tr $SEP "@@@" | awk -F "TESTS THAT DID " '{ print $3 }'| tr "@@@" $SEP >> ../../../../../www/${LCG_NGT_SLT_NAME}.${WEEKDAY}_${LCG_package_config_version}-$CMTCONFIG-qmtest.brief.log

   date >> ../../../logs/$CMTCONFIG-qmtest.log

fi


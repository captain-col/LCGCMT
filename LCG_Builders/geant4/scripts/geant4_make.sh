#!/bin/sh

if test $LCG_NGT_SLT_NAME == "g4tags" ; then
  
   /bin/sh $LCG_package_root/scripts/geant4_cmake.sh  $*

else


   export XERCESCROOT=$VARXERCESCROOT
   date
   echo CLHEP_BASE_DIR=$CLHEP_BASE_DIR
   echo XERCESCROOT=$XERCESCROOT
   echo 

   g++ -v
   echo $PATH

   echo "***********************************************"
   echo "****************** USED TAGS ******************"
   echo "***********************************************"
   cat ${G4INSTALL}/gettags.txt
   echo "***********************************************"


   cd ${G4INSTALL}/source
   ${geant4_pre_make_step}
   make -j 4 
   ${geant4_post_make_step}
   date

fi

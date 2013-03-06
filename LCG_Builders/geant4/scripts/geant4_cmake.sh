#!/bin/sh
export XERCESCROOT=$VARXERCESCROOT
date
echo CLHEP_BASE_DIR=$CLHEP_BASE_DIR
echo XERCESCROOT=$XERCESCROOT
echo 

g++ -v
echo $PATH

echo "***********************************************"
echo "*****       Experimental cmake build  *********"
echo "***********************************************"
echo "****************** USED TAGS ******************"
echo "***********************************************"
cat ${G4INSTALL}/gettags.txt
echo "***********************************************"



test -d ${G4WORKDIR} || mkdir -p ${G4WORKDIR}
cd ${G4WORKDIR}

cmake -DCLHEP_ROOT_DIR=${CLHEP_BASE_DIR}     \
      -DGEANT4_USE_OPENGL_X11=ON	     \
      -DGEANT4_USE_G3TOG4=ON		     \
      -DXERCESC_ROOT_DIR=${VARXERCESCROOT}   \
      -DCMAKE_INSTALL_PREFIX=${G4WORKDIR}    \
      -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} \
      ${G4INSTALL}

${geant4_pre_make_step}

make install

${geant4_post_make_step}
date


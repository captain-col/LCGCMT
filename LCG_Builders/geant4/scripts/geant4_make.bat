set XERCESCROOT=%VARXERCESCROOT%
date /t && time /t

echo ""
echo "***********************************************"
echo "****************** USED TAGS ******************"
echo "***********************************************"
cat `cygpath -u "%G4INSTALL%/gettags.txt"`
echo "***********************************************"


if  "%LCG_NGT_SLT_NAME%"=="g4tags" call %LCG_package_root%/scripts/geant4_cmake.bat
if  "%LCG_NGT_SLT_NAME%"=="g4tags" goto end

echo ""
echo "***********************************************"
echo "******       CYGWin make build          *******"
echo "***********************************************"
echo ""

cd %G4INSTALL%/source

echo "**** starting pre_make...."

%geant4_pre_make_step%

echo "**** starting make build...."

sh -c "make -j 4 G4INSTALL=`cygpath -m $G4INSTALL` G4WORKDIR=`cygpath -m $G4WORKDIR` G4BIN=`cygpath -m $G4BIN` G4TMP=`cygpath -m $G4TMP` G4LIB=`cygpath -m $G4LIB`"

echo "***** make done ****"

%geant4_post_make_step%

:end

date /t

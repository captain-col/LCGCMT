date /t && time /t

echo "************************************************"
echo "***** starting cmake build                 *****"
echo "************************************************"

set PATH=C:\Program Files\CMake 2.8\bin;%PATH%

echo %PATH%

if NOT EXIST %G4WORKDIR% mkdir %G4WORKDIR%

cd %G4WORKDIR%

dir

cmake -G "NMake Makefiles" -DCLHEP_ROOT_DIR="%CLHEP_BASE_DIR%" -DCMAKE_INSTALL_PREFIX=%G4WORKDIR% -DCMAKE_BUILD_TYPE=%CMAKE_BUILD_TYPE% %G4INSTALL%

nmake install

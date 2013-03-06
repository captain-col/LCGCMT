#!/bin/sh

echo "-----------------------------------------------------"
echo "Removing -no-gcc option from CXXFLAGS in config file."

# Change icc compilation options for geant4 + icc
cd $G4INSTALL/config/sys/
mv Linux-icc.gmk Linux-icc.gmk_ORIG

sed -e '/CXXFLAGS/s/-no-gcc//' Linux-icc.gmk_ORIG > Linux-icc.gmk

echo "---done----------------------------------------------"

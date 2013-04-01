#!/bin/sh

if [ ! -x /usr/bin/qmake ]; then
    echo GEANT4 Setup: QT not available
    export CMTEXTRATAGS
    CMTEXTRATAGS="`echo $CMTEXTRATAGS | sed 's/,*GEANT_NO_QT//g'`,GEANT_NO_QT"
fi

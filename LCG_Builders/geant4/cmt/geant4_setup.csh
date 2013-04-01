#!/bin/csh

if ( ! -x /usr/bin/qmake ) then
    echo GEANT4 Setup: QT not available
    setenv CMTEXTRATAGS "`echo $CMTEXTRATAGS | sed 's/,*GEANT_NO_QT//g'`,GEANT_NO_QT"
endif

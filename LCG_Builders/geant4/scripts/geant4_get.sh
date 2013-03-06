#!/bin/sh
# Usage:
#   csh: spi_updt.sh  >& something.log
#    sh: spi_updt.sh  > something.log 2>&1

# .sdb files have a special format
# Must first checkout the head



OS=`uname`

mkdir -p  ${LCG_builddir}/${LCG_package_config_version}

cd  ${LCG_builddir}/${LCG_package_config_version}

if [ x$OS = xDarwin ]
then
   lwp-download http://geant4.cern.ch/cgi-bin/bonsai/nightly/gettaglist.cgi current_bonsai.sdb
   [ $? -ne 0 ] && exit
else
   wget -q http://geant4.cern.ch/cgi-bin/bonsai/nightly/gettaglist.cgi -O current_bonsai.sdb
   [ $? -ne 0 ] && exit
fi


export CVS_RSH=ssh
if [ x$OS = xDarwin ]
then
   protocol=ext
else
   protocol=kserver
fi
      
   export CVSROOT=:${protocol}:$USER@geant4.cvs.cern.ch:/cvs/Geant4

cvs checkout  -l geant4

cd geant4

cat   ../current_bonsai.sdb |
#exec < ../current_bonsai.sdb

while read module tag comments
do
    command="cvs -qq update -d -P -r $tag $module"
    if [ x$module = x\# -o x$module = x ]
    then
        echo Ignore: $tag $comments
    else
        echo $command
        $command
    fi
done


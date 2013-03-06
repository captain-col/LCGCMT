#!/bin/sh

# variables
lcg_vers=56
lcg_home=/afs/cern.ch/sw/lcg
cmt_vers=v1r20p20070524
cmt_site=CERN

# Setup cmt if necessary
{ mycmtver=`cmt version`; } > /dev/null 2>& 1
if [ -z ${mycmtver} ] || [ ${mycmtver} != ${cmt_vers} ]
then eval ". ${lcg_home}/external/CMT/${cmt_vers}/mgr/setup.sh"
fi

export CMTPROJECTPATH=${lcg_home}/app/releases
export CMTPATH=${lcg_home}/app/releases/LCGCMT/LCGCMT_${lcg_vers}
export CMTSITE=${cmt_site}

# Setup any further packages
for pkg in $*; do eval `cmt setup -sh -path=${lcg_home}/app/releases/LCGCMT/LCGCMT_56/LCG_Interfaces -pack=${pkg}` ; done

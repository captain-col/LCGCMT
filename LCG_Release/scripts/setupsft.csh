#!/usr/bin/env tcsh

# variables
set lcg_vers=56
set lcg_home=/afs/cern.ch/sw/lcg
set cmt_vers=v1r20p20070524
set cmt_site=CERN

# Setup cmt if necessary
set mycmtver=`cmt version >>& /dev/stdout`
if ( "${mycmtver}" != "${cmt_vers}" ) then 
  source "${lcg_home}/external/CMT/${cmt_vers}/mgr/setup.csh"
endif

setenv CMTPROJECTPATH ${lcg_home}/app/releases
setenv CMTPATH ${lcg_home}/app/releases/LCGCMT/LCGCMT_${lcg_vers}
setenv CMTSITE ${cmt_site}

# Setup any further packages
foreach pkg ( $argv ) 
  eval `cmt setup -csh -path=${lcg_home}/app/releases/LCGCMT/LCGCMT_56/LCG_Interfaces -pack=${pkg} | tr "\n" "; "`
end

#!/bin/sh

lcg_destdir=$1
lcg_lcghome=$2
lcg_cmtver=$3
lcg_lcgcmtroot=$4

if [ ! -d ${lcg_destdir} ] ; then mkdir -p ${lcg_destdir}; fi 
cd ${lcg_destdir}

cat > setuplcg.sh << EOF
#!/bin/sh

# Setup cmt if necessary
{ mycmtver=\`cmt version\`; } > /dev/null 2>& 1
if [ -z \${mycmtver} ] || [ \${mycmtver} != ${lcg_cmtver} ]
then eval ". ${lcg_lcghome}/external/CMT/${lcg_cmtver}/mgr/setup.sh"
fi

# Setup any further packages
for pkg in \$*; do eval \`cmt setup -sh -path=${lcg_lcgcmtroot}/LCG_Interfaces -pack=\${pkg}\` ; done
EOF


cat > setuplcg.csh << EOF
#!/usr/bin/env tcsh

# Setup cmt if necessary
set mycmtver=\`cmt version >>& /dev/stdout\`
if ( "\${mycmtver}" != "${lcg_cmtver}" ) then 
  source "${lcg_lcghome}/external/CMT/${lcg_cmtver}/mgr/setup.csh"
endif

# Setup any further packages
foreach pkg ( \$argv ) 
  eval \`cmt setup -csh -path=${lcg_lcgcmtroot}/LCG_Interfaces -pack=\${pkg} | tr "\n" "; "\`
end
EOF

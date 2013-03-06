#!/bin/sh

cd ${LCG_builddir}/4Suite-XML-${LCG_package_config_version}
python setup.py install --prefix ${LCG_destbindir}

# make __config__ relocateable
CFGFILE=${LCG_destbindir}/lib/python${LCG_Python_config_version_twodigit}/site-packages/Ft/__config__.py
mv ${CFGFILE} ${CFGFILE}.org
echo "LCG_Ft_home='/'.join(__file__.split('/')[:-5])" >> ${CFGFILE}
cat ${CFGFILE}.org >> ${CFGFILE}
sed s%\'${LCG_destbindir}%LCG_Ft_home+\'% ${CFGFILE} > ${CFGFILE}.new
mv ${CFGFILE}.new  ${CFGFILE}

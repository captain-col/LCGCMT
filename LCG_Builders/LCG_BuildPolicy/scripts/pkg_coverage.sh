#!/bin/bash

# settings for lcov are taken from the file lcovrc, a file ~/.lcovrc overwrites the default settings
# A file ~lcgnight/.lcovrc has been created to overwrite the settings for the coverage ratings

# should look like this ".../slc4_amd64_gcc43_cov/Wed_CORAL_2_0_2-slc4_amd64_gcc43_cov/
[[ -z ${LCG_coverage_result_dir}  ]] && echo ERROR: Directory for code coverage results does not exists! && exit 1
[[ -z ${LCG_NGT_SLT_NAME} ]] && LCG_NGT_SLT_NAME="unknown"
RESULT_DIR=${LCG_coverage_result_dir}/${LCG_NGT_SLT_NAME}.`date +"%a"`_${LCG_pkgdest_vername}-${LCG_CMTCONFIG}/
[[ -d $RESULT_DIR  ]] || mkdir -p $RESULT_DIR


case "$LCG_package" in 
	ROOT)
		cd ${LCG_builddir}/ROOT/${LCG_CheckoutDir}/root

		RESULT_FILE="$RESULT_DIR"/root.info
		lcov -b `pwd` -d `pwd` -c --output-file $RESULT_FILE  --gcov-tool "$GCOV_TOOL" 

		#remove coverage of external code
		#first 3 .cxx files are removed because make process deletes them anyway and gathering their data ends with error
		lcov -r "$RESULT_FILE" "*/rootcint7_tmp.cxx" "*/rootcint_tmp.cxx" "*/RStl_tmp.cxx"  "*afs/cern.ch/sw/lcg/*" "*/usr/include*" -o "$RESULT_FILE"
		;;

	GAUDI|GAUDIATLAS)
		cd ${LCG_builddir}/$LCG_package/${LCG_package_config_version}/GaudiRelease/cmt
		cmt config
		. ./setup.sh

		#collect data
		cmt broadcast -global -select="/${LCG_package_config_version}/" - bash  ${LCG_BUILDPOLICYROOT_DIR}/scripts/collect_data.sh "${RESULT_DIR}"
		;;

	*)
		cd ${LCG_builddir}/$LCG_package/${LCG_package_config_version}/src/config/cmt
		cmt config
		. ./setup.sh

		#collect data
		cmt broadcast -global -select="/${LCG_package_config_version}/" - bash  ${LCG_BUILDPOLICYROOT_DIR}/scripts/collect_data.sh "${RESULT_DIR}"
                # workaround to get rid of mistakenly filled file
                rm -f "${RESULT_DIR}"/Gaudi.info
		;;
esac

#generate html output
echo Remove false positives in "${RESULT_DIR}"
rm -f "${RESULT_DIR}"/Gaudi.info
echo Generating html output from .info files
SPACE=""
genhtml  `find "${RESULT_DIR}" -maxdepth 1 -name \*.info ! -size 0` --output-directory "${RESULT_DIR}" --title "${LCG_package} code coverage" --show-details --legend   | tee "${RESULT_DIR}"/genhtml.log

#genhtml ended without error
if [[ "$?" == 0 ]];then
	RESULT=
	rate=`cat "${RESULT_DIR}"/genhtml.log | tail -4 | head -1 `
	if [[ x"$rate" == x"Overall coverage rate:" ]];then
		#generated html has correct format
		lines=`cat "${RESULT_DIR}"/genhtml.log | tail -3 | head -1 | cut -d" " -f4`
		funcs=`cat "${RESULT_DIR}"/genhtml.log | tail -2 | head -1 | cut -d" " -f4`
		branches=`cat "${RESULT_DIR}"/genhtml.log | tail -1 | head -2 | cut -d" " -f4`
		RESULT="${lines}, ${funcs}, ${branches}"
	else
		#generated html has NOT correct format
		RESULT="N/A%, N/A%,N/A%"
	fi

	echo "$RESULT" >> ${LCG_coverage_result_dir}/${LCG_NGT_SLT_NAME}.`date +"%a"`_${LCG_pkgdest_vername}-${LCG_CMTCONFIG}-log.summary
fi

#cleaning little bit
#rm -f "${RESULT_DIR}"/*.info


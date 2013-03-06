#!/bin/bash

# get name of package from path
package=`echo \`pwd\` | sed 's|^.*/\([a-zA-Z0-9]*\)/cmt$|\1|'`
#package=${LCG_package}

if [[ -z "$1" ]];then
	RESULT_DIR=/tmp/results
else
	RESULT_DIR="$1"
fi
RESULT_FILE="${RESULT_DIR}/${package}.info"
LOG_FILE="${RESULT_DIR}/${package}_lcov.log"


# we don't care about coverage of tests 
[[ "$package" == *"Tests"* ]] && exit

# test if .gcno and .gcda files are created in this package
[[ `ls ../"$CMTCONFIG"/*gcno | wc -l 2>/dev/null` -le 0 ]] && echo No .gcno files! && exit 
[[ `ls ../"$CMTCONFIG"/*gcda | wc -l 2>/dev/null` -le 0 ]] && echo No .gcda files! && exit 

# collet coverage data from gcda files
lcov -d `pwd`/.. -c -o "$RESULT_FILE"  --gcov-tool "$GCOV_TOOL" --test-name "$package testing" >>  $LOG_FILE

# problematic file, not needed for coverage
lcov -r "$RESULT_FILE" "*/input.gperf" "*/tests/*" "*_rflx.cpp" -o "$RESULT_FILE" >>  $LOG_FILE


# ignore coverage of external code
lcov -e "$RESULT_FILE"  "*/${LCG_package}/*" -o "$RESULT_FILE" >>  $LOG_FILE



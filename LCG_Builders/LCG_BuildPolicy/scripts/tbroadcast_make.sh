#!/bin/sh

LCG_PKG_LOG=${LCG_builddir}/${LCG_package}/${LCG_package_config_version}

LCG_SORTFILE=${LCG_BUILDPOLICYROOT_DIR}/scripts

mkdir -p ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$3
mkdir -p ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$4
mkdir -p ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$5


tbroadcast -output=${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$3  -nb=$1 -local "lockfile cmt_package.lock; cmt make -j$1 -l$2 $3 ; rm -f cmt_package.lock"
tbroadcast -output=${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$4  -nb=$1 -local "lockfile cmt_package.lock; cmt make -j$1 -l$2 $4 ; rm -f cmt_package.lock"
tbroadcast -output=${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$5  -nb=$1 -local "lockfile cmt_package.lock; cmt make -j$1 -l$2 $5 ; rm -f cmt_package.lock"


#Concatenate files under all directory
cd  ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$3
for file in *; do
    bar=`expr substr $file 1 5`
    if [ "$bar" != "error" ]; then
	cat "$file" >>"${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$3/$file.templog"
    fi
done
#Concatenate files under utilities directory
cd  ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$4
for file in  *; do
    bar=`expr substr $file 1 5`
    if [ "$bar" != "error" ]; then
	cat "$file">>"${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$4/$file.templog"
    fi
done

#Concatenate files under tests directory
cd  ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$5
for file in *; do
    bar=`expr substr $file 1 5`
    if [ "$bar" != "error" ]; then
        cat "$file" >>"${LCG_PKG_LOG}/${LCG_CMTCONFIG}/$5/$file.templog"
    fi 
done



cat ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/*/*.templog>>${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log
python ${LCG_SORTFILE}/sortFile.py --target=all --file=${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log
python ${LCG_SORTFILE}/sortFile.py --target=utilities --file=${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log
python ${LCG_SORTFILE}/sortFile.py --target=tests --file=${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log

rm ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log
date >>${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log
cat ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.logall ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.logtests ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.logutilities>>${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log

mkdir -p ${LCG_PKG_LOG}/logs/

mv ${LCG_PKG_LOG}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log ${LCG_PKG_LOG}/logs/${LCG_CMTCONFIG}.log






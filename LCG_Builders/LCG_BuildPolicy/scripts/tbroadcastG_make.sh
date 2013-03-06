#!/bin/sh



 mkdir ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}
 mkdir ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$2
 mkdir ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$3
 mkdir ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$4
  
tbroadcast -output=${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$2 -error=${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$2 -nb=$1 -local 'lockfile cmt_package.lock ;cmt make -j$1 $2; rm -f cmt_package.lock' 
tbroadcast -output=${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$3 -error=${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$3 -nb=$1 -local 'lockfile cmt_package.lock; cmt make -j$1 $3; rm -f cmt_package.lock'
tbroadcast -output=${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$4 -error=${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$4 -nb=$1 -local 'lockfile cmt_package.lock;cmt make -j$1 $4; rm -f cmt_package.lock'

cd  ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$2

   #Concatenate files under all directory
for file in *; do
    bar=`expr substr $file 1 5`
    if [ "$bar" != "error" ]; then
	cat "$file" "error$file">>"${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$2/$file.templog"
    fi
 
done

 cd  ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$3

#Concatenate files under tests directory
for file in  *; do
    bar=`expr substr $file 1 5`
    if [ "$bar" != "error" ]; then
	cat "$file" "error$file">>"${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$3/$file.templog"
    fi
 
done

cd  ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$4

#Concatenate files under utilities directory
for file in *; do

   bar=`expr substr $file 1 5`
    if [ "$bar" != "error" ]; then
	cat "$file" "error$file">>"${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/$4/$file.templog"
    fi
 
done

cat  ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/*/*.templog>>${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log
mv ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}.log ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}.loglog
cp ${LCG_PKG_LOG_GAUDI_DIR}/${LCG_CMTCONFIG}/${LCG_CMTCONFIG}.log  ${LCG_PKG_LOG_GAUDI_DIR}
dir


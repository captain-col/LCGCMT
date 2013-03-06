#!/bin/sh

cd ${LCG_builddir}

rpm2cpio dcache-srmclient-${LCG_dcache_srm_version}.noarch.rpm | cpio -idv
rpm2cpio dcap-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv

if [[ $CMTCONFIG == *slc6* ]]; then
    rpm2cpio dcap-libs-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio dcap-devel-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio dcap-tunnel-gsi-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio dcap-tunnel-krb-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio dcap-tunnel-ssl-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio dcap-tunnel-telnet-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
fi

if [[ $CMTCONFIG == *slc5* ]]; then
    rpm2cpio dcap-tests-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio libdcap-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio libdcap-devel-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio libdcap-tunnel-gsi-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio libdcap-tunnel-krb-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio libdcap-tunnel-ssl-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
    rpm2cpio libdcap-tunnel-telnet-${LCG_dcache_dcap_version}${LCG_dcache_arch}.rpm | cpio -idv
fi

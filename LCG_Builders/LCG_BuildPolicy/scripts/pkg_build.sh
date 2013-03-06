#!/bin/sh

rm -fr ${LCG_builddir}/*
cmt pkg_get
cmt pkg_config
cmt pkg_make 
cmt pkg_install
cmt pkg_loginstall

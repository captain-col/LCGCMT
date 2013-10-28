#!/bin/sh

which fs > /dev/null
if [ "x$?" = "x0" ] ; then
    fs checkservers
    fs checkvolumes
fi


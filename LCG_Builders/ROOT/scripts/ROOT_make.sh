#!/bin/sh

date

# Set the maximum load during the job.  This can be overridden in the
# environment.
if [ "x$LCG_MAX_LOAD" = "x" ]; then
    LCG_MAX_LOAD=2.5
fi
echo Limit load to ${LCG_MAX_LOAD}

cd ${LCG_destbindir}/${LCG_srcdir}

# Build the main root package
make -k -l ${LCG_MAX_LOAD} -j

# Now build the tests.
# cd test
# make -k -l ${LCG_MAX_LOAD} -j

date

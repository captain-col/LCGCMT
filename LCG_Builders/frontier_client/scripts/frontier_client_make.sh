#!/bin/sh

cd ${LCG_builddir}/frontier_client__${LCG_package_config_version}__src
${LCG_frontier_compile_options}
make dist EXPAT_DIR=${LCG_expat_dir} DEBUG_OPTIM="-g -O2 ${CFLAGS}"

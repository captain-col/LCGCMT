#!/bin/sh
cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd SDL_ttf-${LCG_package_config_version}
./configure --prefix=${LCG_destbindir} ${LCG_sdl_config_opts}

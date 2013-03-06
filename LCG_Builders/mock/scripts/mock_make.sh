#!/bin/sh

cd ${LCG_builddir}/mock-${LCG_package_config_version}
${LCG_mock_compile_options}
python setup.py build

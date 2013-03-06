#!/bin/sh

cd ${LCG_builddir}/SQLAlchemy-${LCG_package_config_version}
${LCG_sqlalchemy_compile_options}
python setup.py build

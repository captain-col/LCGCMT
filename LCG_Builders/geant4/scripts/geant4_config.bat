cd %LCG_builddir%
if exist %LCG_tarfilename% (
if not exist %LCG_package% mkdir %LCG_package%
cd %LCG_package%
tar xvfz ../%LCG_tarfilename%
)
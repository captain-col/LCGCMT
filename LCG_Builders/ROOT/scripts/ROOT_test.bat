set PATH=%ROOTSYS%\bin:%PATH%

cd %LCG_builddir%\ROOT\%LCG_CheckoutDir%\roottest
set PWD=%LCG_builddir%\ROOT\%LCG_CheckoutDir%\root\roottest
echo %DATE% %TIME%
sh -c "make -k"

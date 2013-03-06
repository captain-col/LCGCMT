set PATH=C:\cygwin\bin;%PATH%
cd %LCG_builddir%\ROOT\%LCG_CheckoutDir%\root
echo %DATE% %TIME%
svn info
sh -c "make -k"
sh -c "make -k cintdlls"
cd %LCG_builddir%\ROOT\%LCG_CheckoutDir%\root\test

sh -c "make -k"
cd %LCG_builddir%\ROOT\%LCG_CheckoutDir%\root

sh -c "make -k map"


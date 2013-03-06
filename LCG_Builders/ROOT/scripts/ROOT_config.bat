set PATH=C:\cygwin\bin;%PATH%
cd %LCG_builddir%\ROOT\%LCG_CheckoutDir%\root
echo %DATE% %TIME%
sh -c './configure %LCG_ROOT_CONFIG_ARCH% %LCG_ROOT_CONFIG_OPTIONS%'

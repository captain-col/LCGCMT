cd %LCG_builddir%\boost_%LCG_package_file_config_version%
"%LCG_bjam_bin%" %LCG_boost_jam_opts% --toolset=%LCG_boost_toolset% --user-config=user-config.jam

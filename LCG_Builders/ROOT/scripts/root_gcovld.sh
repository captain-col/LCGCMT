#!/bin/bash
# easist way how to link all files of ROOT with lgcov library
# for code coverage ROOT is configured with param --with-ld="this_script"
g++ "$@" -lgcov

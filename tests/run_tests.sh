# !/bin/bash

# Return error if any script returns a non-zero exit code.
set -e

# perform lint test for all files
pylint -r n --disable=fixme --output-format=colorized smile tests/python/ setup.py

# perform nosetests
PYTHONPATH=`pwd` nosetests

# !/bin/bash

# Return error if any script returns a non-zero exit code.
set -eu

# perform lint test for all files
pylint -r n --disable=fixme --output-format=colorized smile tests/python/ \
setup.py tests/smoke_tests/smoke_test.py

# perform nosetests
PYTHONPATH=`pwd` nosetests

# run smoke tests.
bash tests/smoke_tests/smoke_test.sh

# Indicate all tests have passed.
echo "All tests passed."

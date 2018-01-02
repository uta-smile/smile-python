#!/bin/bash

set -eu

echo "Starting smoke tests..."
DIR="$( cd "$( dirname "$0" )" && pwd )"
SMOKE_TEST_PY="${DIR}/smoke_test.py"

RET=`python $SMOKE_TEST_PY 2>&1`
echo $RET | grep 'param = default_value'

echo "Smoke tests passed."

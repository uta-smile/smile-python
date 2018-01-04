#!/bin/bash

set -eu

echo "Starting smoke tests..."
DIR="$( cd "$( dirname "$0" )" && pwd )"
SMOKE_TEST_PY="${DIR}/smoke_test.py"

RET=`python $SMOKE_TEST_PY echo --echo_text "hello world!" 2>&1`
echo $RET | grep 'param = default_value'
echo $RET | grep 'hello world!'

python $SMOKE_TEST_PY echo_bool 2>&1 | grep "Just do it? No :("
python $SMOKE_TEST_PY echo_bool --just_do_it 2>&1 | grep "Just do it? Yes!"

echo "Smoke tests passed."

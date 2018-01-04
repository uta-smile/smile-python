#!/bin/bash

set -eu

echo "Starting smoke tests..."
DIR="$( cd "$( dirname "$0" )" && pwd )"
SMOKE_TEST_PY="${DIR}/smoke_test.py"

RET=`python $SMOKE_TEST_PY echo --echo_text "hello world!" 2>&1`
echo $RET | grep 'param = default_value'
echo $RET | grep 'hello world!'

RET=`python $SMOKE_TEST_PY echo --echo_text "hello world!" --verbosity -1 2>&1`
echo $RET | grep 'hello world!'

# Shoud not generate any output.
python $SMOKE_TEST_PY --param "new_value" echo_bool --verbosity -1 2>&1

RET=`python $SMOKE_TEST_PY --param "new_value" echo_bool --just_do_it 2>&1`
echo $RET | grep 'param = new_value'
echo $RET | grep 'Just do it? Yes!'

python $SMOKE_TEST_PY echo_bool 2>&1 | grep "Just do it? No :("
python $SMOKE_TEST_PY echo_bool --just_do_it 2>&1 | grep "Just do it? Yes!"

echo "Smoke tests passed."

#!/bin/bash

# This script has to run in the root folder of Dataracebench.

TESTS=($(grep -l main micro-benchmarks/*.cpp micro-benchmarks/*.c))
for test in "${TESTS[@]}"; do
  testname=$(basename $test)
  id=${testname#DRB}
  id=${id%%-*}
  echo "$test has $testname and ID=$id"
  curl -F "file=@\"$test\"" localhost:5010/test?type=json
done

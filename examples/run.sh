#!/bin/bash

cd `dirname $0`

for filename in *.py; do
    output=${filename%.*}_out.txt
    echo "Running $filename... (result $output)"
    $PYTHON_HOME/bin/python $filename > $output 2>&1
done

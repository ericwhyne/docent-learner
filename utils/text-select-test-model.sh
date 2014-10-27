#!/bin/bash
line=`shuf -n 1 ../tmp/text-select.vw`; echo $line; echo $line | vw -i ../tmp/text-select-svm.model -p /dev/stdout --quiet

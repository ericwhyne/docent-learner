#!/bin/bash
./text-select-to-vw.py > ../tmp/text-select.vw
vw ../tmp/text-select.vw -c --passes 25 --loss_function hinge -f ../tmp/text-select-svm.model

#!/usr/bin/python
import subprocess

predict_command = ("ls -l").split(' ')

out = subprocess.check_output(predict_command)
print out

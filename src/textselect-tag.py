#!/usr/bin/python
import subprocess
import sys
import nltk
import re
import docent_learner_vw as dlvw

infile = sys.stdin
text = infile.read()

textwords = text.split(' ')
textbiwords = dlvw.bigrams(textwords)
texttriwords = nltk.trigrams(textwords)

candidates = []
for word in textwords:
  candidates.append(dlvw.features(word, "0"))
for biword in textbiwords:
  s = biword[0] + '_' + biword[1]
  dlvw.features(s,"0")
for triword in texttriwords:
  s = triword[0] + '_' + triword[1] + '_' + triword[2]
  dlvw.features(s,"0")

for candidate in candidates:
  print candidate
  #TODO put the actual vw command in this placeholder
  predict_command = "echo \"" + candidate + "\" | vw -i ../tmp/text-select-svm.model -p /dev/stdout --quiet"
  out = subprocess.check_output(predict_command.split(' '))
  print predict_command.split(' ')
  print out

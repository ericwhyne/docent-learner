#!/usr/bin/python
import os
import re
import json
import nltk
import string
import docent_learner_vw as dlvw
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

textselect_dir = "/var/www/html/docent-learner/textselect/"

def list_json_files(json_dir):
  jsonfiles = [f for f in os.listdir(json_dir) if re.match(r'.*\.json$', f,  re.IGNORECASE)]
  return jsonfiles

for fn in list_json_files(textselect_dir):
  tags = json.loads(open(textselect_dir + fn, 'r').read())
  try:
    selected = tags['selected_text']
  except:
    selected = ''
  text_fn = tags['tagged_text_filename']
  text = re.sub('\n','',open(textselect_dir + text_fn, 'r').read())
  text_sans_selected = re.sub(re.escape(selected),'',text)
  words = text_sans_selected.split(' ')

  selectedwords = selected.split(' ')
  selectedbigrams = dlvw.bigrams(selectedwords)
  selectedtrigrams = nltk.trigrams(selectedwords)

  textwords = text_sans_selected.split(' ')
  textbiwords = dlvw.bigrams(textwords)
  texttriwords = nltk.trigrams(textwords)

  # print positive examples
  if selected != '':
    print dlvw.features(re.sub(' ','_',selected), "1")

  #TODO account for negative examples that exist within selected text (incomplete subsets of selection)

  # print negative examples
  for word in textwords:
    print dlvw.features(word, "-1")
  for biword in textbiwords:
    s = biword[0] + '_' + biword[1]
    print dlvw.features(s,"-1")
  for triword in texttriwords:
    s = triword[0] + '_' + triword[1] + '_' + triword[2]
    print dlvw.features(s,"-1")

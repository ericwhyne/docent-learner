#!/usr/bin/python
import os
import re
import json
import nltk
import string
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

textselect_dir = "/var/www/html/docent-learner/textselect/"

# counts instances of l2 in l1
count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))

def list_json_files(json_dir):
  jsonfiles = [f for f in os.listdir(json_dir) if re.match(r'.*\.json$', f,  re.IGNORECASE)]
  return jsonfiles

def bigrams(input_list):
  return zip(input_list, input_list[1:])

def print_features(s, cat):
  features = cat + " | "
  # length of the string
  features += "l:" + str(len(s)) + ' '
  # number of numerical characters in the string
  s_digits =  count(s, string.digits)
  features += "d:" + str(s_digits) + ' '
  # number of punctuation in the string
  s_punct = count(s, string.punctuation)
  features += "p:" + str(s_punct) + ' '
  # the trigrams
  feature_trigrams = ''
  for trigram in nltk.trigrams(s):
    feature_trigrams += trigram[0] + trigram[1] + trigram[2] + " "
  features += feature_trigrams 
  # the bigrams
  feature_bigrams = ''
  for bigram in bigrams(s):
    feature_bigrams += bigram[0] + bigram [1] + " "
  features += feature_bigrams
  # every character
  chars = ''
  for char in s:
    chars += char + " "
  features += chars
  print features 



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
  selectedbigrams = bigrams(selectedwords)
  selectedtrigrams = nltk.trigrams(selectedwords)
  
  textwords = text_sans_selected.split(' ')
  textbiwords = bigrams(textwords)
  texttriwords = nltk.trigrams(textwords)
 
  # print positive examples
  if selected != '':
    print_features(re.sub(' ','_',selected), "1")

  #TODO account for negative examples that exist within selected text (incomplete subsets of selection)

  # print negative examples
  for word in textwords:
    print_features(word, "-1")
  for biword in textbiwords:
    s = biword[0] + '_' + biword[1]
    print_features(s,"-1")
  for triword in texttriwords:
    s = triword[0] + '_' + triword[1] + '_' + triword[2]
    print_features(s,"-1")


  


    

  
 
  

#!/usr/bin/python
import re
import nltk
import string
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

# counts instances of l2 in l1
count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))

def bigrams(input_list):
  return zip(input_list, input_list[1:])

def features(s, cat):
  s = re.sub('\||:|\s', '', s) # Remove vertical bar, colon, space, and newline; unsupported by vw file format
  features = ''
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
  features = cat + " | " + features
  return features

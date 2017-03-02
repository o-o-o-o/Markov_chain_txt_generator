#!/usr/bin/python

import numpy as np
import sys
import collections    #for the counter

if (len(sys.argv) < 3):
   print "Usage: markov_text_generation.py [order] [input file path] [num characters]"
   sys.exit()

#optionally seed the PRNG
#np.random.seed(12)

#The file name to open to generate the distribtions
TEXT_FILE_NAME = sys.argv[2]

#Condition the probabilties the the previous ORDER number of characters
ORDER = int(sys.argv[1])

#How many characters long we want the resultant markov chain to contain
LENGTH = int(sys.argv[3])

# Open a text file. This text file is the training corpus.
input_text_file = open(TEXT_FILE_NAME, 'r')
input_text = input_text_file.read()
TEXT_SEED = input_text[:ORDER]

# Create a dictionary where the keys are the prefixes (strings of #{ORDER} consecutive characters) 
#   and the values are a counter of suffixes (the character immediately following the prefix).
# 
# For example: dict = {'the b': Counter({'e': 3, 'a': 2, 'i': 1}),
#                      'he be': Counter({'s': 1, 'l': 1, 'e': 1}), ...}
def get_prefix_counts(order):
   global input_text
   prefix_suffix_dict = {}
   for i in range( len(input_text) - order):
      new_key = input_text[i:i+order]
      if not prefix_suffix_dict.has_key(new_key):
         prefix_suffix_dict[new_key] = collections.Counter()
      prefix_suffix_dict[new_key][input_text[i+order]] += 1      
   return prefix_suffix_dict

def choose_letter(prefix):
   global text_stats
   x = np.array([float(value) for value in text_stats[prefix].values()])
   x = x/x.sum()
   y = np.random.choice(text_stats[prefix].keys(), 1, p=x)
   return y

start = TEXT_SEED[:ORDER]
text_stats = get_prefix_counts(ORDER)
for i in np.arange(LENGTH):
    start += choose_letter(start[i+0:i+ORDER])[0]
print '\n\n'
print start


from corpusMethods import *
import math as m
import random
from collections import Counter

# Choose words
WORD = {'TRAIN', 'TRAINS', 'TRAINED','TRAINING'}
seed1 = {'STATION', 'STATIONS', 'RAILS', 'RAIL', 'DESTINATION', 'WAGON',
         'WAGONS'}
seed2 = {'MUSCLES', 'MUSCLE', 'WEIGHT', 'WEIGHTS', 'SPORT', 'SPORTS'}
SEARCH_WINDOW = 2
A = []
B = []

# Read corpus
ignore = {'\'', '"', '.', ',', '/', '\\', '(', ')',';'}

corp = readCorpus('corpus_ex1')
corp = extractSentences('<s>', '</s>' ,corp, ignore)

# Find basic collocations
sentences = []
for sentence in corp:
    for w in WORD:
        if w in sentence:
            indices = [index for index, value in enumerate(sentence) if
                        value == w]
            for i in indices:
                s = max(i-SEARCH_WINDOW,0)
                e = min(i+SEARCH_WINDOW, len(sentence))
                cur = sentence[s:e]
                st = set(cur)
                st.remove(w)
                if len(st & seed1) > 0:
                    A.append(sentence[max(i - 3*SEARCH_WINDOW, 0):min(i +
                                                           3*SEARCH_WINDOW,
                                                           len(sentence))])
                elif len(st & seed2) > 0:
                    B.append(sentence[max(i - 3*SEARCH_WINDOW, 0):min(i +
                                                           3*SEARCH_WINDOW,
                                                           len(sentence))])
def printSentences(a, lst):
    for l in lst:
        print(a, ':\t', end='')
        for w in l:
            print(w, end=' ')
        print()

printSentences('A',A)
printSentences('B',B)
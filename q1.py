from corpusMethods import *
import math as m
import random
from collections import Counter

# Choose words
WORD = {'PLANT'}
seed1 = {'LIFE', 'LIVES'}
seed2 = {'MANUFACTURE', 'MANUFACTURING', 'MANUFACTURED'}
SEARCH_WINDOW = 4
THRESHOLD_SCORE = 0.7
THRESHOLD_FREQ = 5
TRAINING_SET_SIZE = 200

# Read corpus
ignore = {'\'', '"', '.', ',', '/', '\\', '(', ')',';'}

corp = readCorpus('corpus_ex1')
corp = extractSentences('<s>', '</s>' ,corp, ignore)

# Find basic collocations
reducesSentences = []
for sentence in corp:
    for w in WORD:
        if w in sentence:
            indices = [index for index, value in enumerate(sentence) if
                        value == w]
            for i in indices:
                s = max(i-SEARCH_WINDOW,0)
                e = min(i+SEARCH_WINDOW, len(sentence))
                cur = sentence[s:e]
                reducesSentences.append(cur)

trainingSet = random.sample(reducesSentences, TRAINING_SET_SIZE)

def tagColloc(sampSet, seedA, seedB, A, B):
    for s in sampSet:
        cur = s
        st = set(s)
        if seedA & st:
            A.append(cur)
        elif seedB & st:
            B.append(cur)

def findingSeeds(tagged, notSeeds):
    potentialSeeds = dict()
    for s in tagged:
        for w in s:
            if w in notSeeds:
                continue
            c = Counter(s)[w]
            if w in potentialSeeds:
                potentialSeeds[w] += c
            else:
                potentialSeeds[w] = c
    return potentialSeeds




def yarovskyAlgo(word, seedA, seedB, sampleSet):
    A = []
    B = []
    ranking = dict()
    notSeeds = set()
    tagColloc(sampleSet, seedA, seedB, A, B)
    potentialSeedsA = findingSeeds(A, notSeeds)
    potentialSeedsB = findingSeeds(B, notSeeds)
    candidates = set(potentialSeedsB.keys()) | set(potentialSeedsA.keys())
    for w in candidates:
        print(w)
        try:
            freqA = potentialSeedsA[w]
        except:
            ranking[w] = '+'
            continue
        try:
            freqB = potentialSeedsB[w]
        except:
            ranking[w] = '-'
            continue
        probA = freqA/(freqB+freqA)
        probB =  freqB/(freqA+freqB)
        ranking[w] = m.log(probA/probB)
    return ranking

print(yarovskyAlgo(WORD, seed1, seed2, reducesSentences))


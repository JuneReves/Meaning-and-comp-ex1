from corpusMethods import *
import math as m
import random
from collections import Counter

# Choose words
WORD = {'ORANGE', 'ORANGES'}
seed1 = {'COLOUR', 'COLOR'}
seed2 = {'FOOD'}
SEARCH_WINDOW = 4
THRESHOLD_SCORE = 0.5
THRESHOLD_FREQ = 3
TRAINING_SET_SIZE = 200
A = []
B = []

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
        sampSet.remove(s)

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




def yarovskyAlgo(seedA, seedB, sampleSet,freqThresh, rankThrash, A, B, i=5):
    ranking = dict()
    notSeeds = set()
    tagColloc(sampleSet, seedA, seedB, A, B)
    found = notSeeds | seedA | seedB
    potentialSeedsA = findingSeeds(A, found)
    potentialSeedsB = findingSeeds(B, found)
    candidates = set(potentialSeedsB.keys()) | set(potentialSeedsA.keys())
    for w in candidates:
        try:
            freqA = potentialSeedsA[w]
        except:
            ranking[w] = -999999
            continue
        try:
            freqB = potentialSeedsB[w]
        except:
            ranking[w] = 999999
            continue
        probA = freqA/(freqB+freqA)
        probB =  freqB/(freqA+freqB)
        ranking[w] = m.log(probA/probB)

        for w in ranking:
            freq = 0
            try:
                freq += potentialSeedsA[w]
            except:
                print(w, 1)
            try:
                freq += potentialSeedsB[w]
            except:
                print(w, 2)
            if freq < freqThresh:
                notSeeds.add(w)
                continue
            if ranking[w] < -rankThrash:
                seedB.add(w)
                continue
            if ranking[w] > rankThrash:
                seedA.add(w)
                continue
            notSeeds.add(w)
        if i == 0 or len(sampleSet) == 0:
            return
        yarovskyAlgo(seedA, seedB, sampleSet, freqThresh, rankThrash,A,B, i-1)

yarovskyAlgo(seed1, seed2, reducesSentences, THRESHOLD_FREQ,
             THRESHOLD_SCORE,A,B, 100)

print(seed1)
print(A)
print(seed2)
print(B)


from corpusMethods import *
import math as m
import random
from collections import Counter

# Choose words
WORD = {'POPULATION', 'POPULATIONS'}
seed1 = {'PEOPLE'}
seed2 = {'BACTERIA', 'BACTERIAL'}
SEARCH_WINDOW = 2
THRESHOLD_SCORE = 0.3
THRESHOLD_FREQ = 2
TRAINING_SET_SIZE = 200
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
            if w in sentence:
                sentences.append(sentence)
            # indices = [index for index, value in enumerate(sentence) if
            #             value == w]
            # for i in indices:
            #     s = max(i-SEARCH_WINDOW,0)
            #     e = min(i+SEARCH_WINDOW, len(sentence))
            #     cur = sentence[s:e]
            #     reducesSentences.append(cur)
try:
    trainingSet = random.sample(sentences, TRAINING_SET_SIZE)
except:
    trainingSet = sentences.copy()


with open('trainingSet', 'w') as file:
    for l in trainingSet:
        line = ''
        for w in l:
            line += w
            line += ' '
        line += '\n'
        file.write(line)


def tagColloc(sampSet, seedA, seedB, A, B, a):
    for s in sampSet:
        indices = [index for index, value in enumerate(s) if
                   (value in seedA or value in seedB)]
        for i in indices:
            sta = max(i - SEARCH_WINDOW, 0)
            e = min(i + SEARCH_WINDOW, len(s))
            cur = s[sta:e]
            st = set(cur)
            if seedA & st:
                A.append(s[max(i - 3*SEARCH_WINDOW, 0):min(i +
                                                           a*SEARCH_WINDOW,
                                                           len(s))])
            elif seedB & st:
                B.append(s[max(i - 3*SEARCH_WINDOW, 0):min(i +
                                                           a*SEARCH_WINDOW,
                                                           len(s))])
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



allSeedsA = dict()
allSeedsB = dict()
ranking = dict()
def yarovskyAlgo(seedA, seedB, sampleSet,freqThresh, rankThrash, A, B, i=5):
    notSeeds = set()
    tagColloc(sampleSet, seedA, seedB, A, B, 3)
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
                pass
            try:
                freq += potentialSeedsB[w]
            except:
                pass
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

yarovskyAlgo(seed1, seed2, trainingSet, THRESHOLD_FREQ,
             THRESHOLD_SCORE,A,B, 100)


def printSentences(a, lst):
    lines = []
    for l in lst:
        line = a + ':\t'
        for w in l:
            line += w + ' '
        lines += '\n'
        lines.append(line)
    return lines

print(seed1)
print(seed2)
print(ranking)

total_A = []
total_B = []


for sentence in sentences:
    indices = [index for index, value in enumerate(sentence) if
               (value in seed1 or value in seed2)]
    for i in indices:
        cur = sentence[max(i-SEARCH_WINDOW, 0):min(i+SEARCH_WINDOW,
                                                   len(sentence))]
        if set(cur) & seed1:
            total_A.append(cur)
        elif set(cur) & seed2:
            total_B.append(cur)

toPrint = []

toPrint += printSentences('A',total_A)
toPrint += printSentences('B',total_B)


with open('q1Sentences', 'w') as file:
    for l in toPrint:
        file.write(l)
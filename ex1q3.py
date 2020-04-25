from nltk.corpus import wordnet
from ex1q1update import will_sent
nltk.tokenize.punkt import PunktSentenceTokenizer
import sys

# From https://github.com/Akirato/Lesk-Algorithm/blob/master/leskAlgorithm.py
# Setting the context's ranking

context_window = ['a', 'the', 'be', 'see' ]

def overlap (synset, sent):
    gloss = set(PunktSentenceTokenizer().tokenize(synset.definition()))

    for word in synset.examples():
        gloss.union(word)

    sent = sent.difference(context_window)

    return len( gloss.intersection(sentence) )

def lesk (word, sentence):
    bestsense = None
    maxoverlap = 0
    word = wordnet.morphy(word)  if wordnet.morphy(word) is not None else word

    for sense in wordnet.synsets(word):
        overlap_rank = overlap(sense, sentence)
        for hyponym in sense.hyponyms():
            overlap_rank += overlap(hyponym, sentence)
        if overlap_rank > maxoverlap:
                maxoverlap = overlap_rank
                bestsense = sense

    return bestsense

# a = lesk(str(context_window),will_sent)
# print ("\n\nSynset: ", a)
# if a is not None:
#     print ("Meaning: ", a.definition())
#     num=0
#     print ("\nExamples: ")
#     for i in a.examples():
#         num=num+1
#         print (str(num) + '.' + ')', i)
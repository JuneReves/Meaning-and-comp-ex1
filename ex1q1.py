import nltk
import string
import re

'''
Question 1:
-----------
The word 'will':
A) Future tense of 'be' (aux. verb)
    I) "The sun will shine tomorrow" (from WordNet)
    II) "Tomorrow morning I will wake up in this first-class hotel suite" (Merriam-Webster)
B) Testament, legal document (noun)
    I) "writing a will before I die."
    II) "Having a will in place is not only for elderly or wealthy people!"
'''

'''Draft
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = ''.join(tokenizer.tokenize(str_corpus))
'''

corpus = open('corpus_ex1', 'rt')
str_corpus = corpus.read().replace('\n', ' ') #Converting the file into strings
corpus.close()

punct = set(string.punctuation)
freqlst = open('corpus_ex1.freq_list', 'r')


#Step one
sentences = [line for line in re.compile('<s>[\w+\s]+</s>').findall(
    str_corpus)]
counter = 0
# for i in re.compile('<s>[\w+\s]+</s>').findall(str_corpus) :
#     if i == '<s>':
#         counter += 1
#         sentences.append(str_corpus[counter:])
#     elif i =='</s>':
#         counter += 1
#         sentences.append(str_corpus[:counter])
#     else:
#         sentences.append(i)
#         counter += 1

print(sentences)


import re

def organizeData():
    with open('corpus_ex1.freq_list', 'r') as f:
        lst = [line.replace('\n', '').split('\t') for
                line in
                f.readlines()]
        data = dict()
        for l in lst:
            data[l[0].upper()]=l[1]
        f.close()
    return data

def searchWordFreq(w, d):
    try:
        return int(d[w.upper()])
    except:
        return None


def sumFreqs():
    reg = re.compile('\d+')
    sum = 0
    with open('corpus_ex1.freq_list', 'r') as f:
        for line in f.readlines():
            sum += int(reg.search(line).group())
    return sum


def readCorpus(f):
    with open(f, 'r') as file:
        lines = file.readlines()
    final = []
    for line in lines:
        final.append(line.replace('\n',''))
    return final

def extractSentences(openTag, closeTag, corpus, ignore):
    sentences = []
    reading = False
    sentence = []
    for l in corpus:
        if l == openTag:
            reading = True
            sentence = []
            continue
        if reading:
            if l != closeTag:
                if l not in ignore:
                    sentence.append(l.upper())
            else:
                sentences.append(sentence)
                reading = False
    return sentences
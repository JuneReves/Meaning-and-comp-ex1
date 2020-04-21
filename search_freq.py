import re

def organizeData():
    with open('corpus_ex1.freq_list', 'r') as f:
        lst = [line.replace('\n', '').split('\t') for
                line in
                f.readlines()]
        data = dict()
        for l in lst:
            data[l[0].capitalize()]=l[1]
        f.close()
    return data

def searchWordFreq(w, d):
    try:
        return int(d[w.capitalize()])
    except:
        return None


def sumFreqs():
    reg = re.compile('\d+')
    sum = 0
    with open('corpus_ex1.freq_list', 'r') as f:
        for line in f.readlines():
            sum += int(reg.search(line).group())
    return sum
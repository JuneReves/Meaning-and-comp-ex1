from nltk.corpus import wordnet as wn
import search_freq
import math

d = search_freq.organizeData()


def chooseFreq(syn):
    w = None
    for word in syn.lemma_names():
        if search_freq.searchWordFreq(word, d) is not None:
            w = search_freq.searchWordFreq(word, d)
            break
    return w

#Get needed synsets form wordnet and list them = set()
root = wn.synset('star.n.01')
firstLevel = set(root.hyponyms())
secondLevel = set()
for syn in firstLevel:
    secondLevel.update(set(syn.hyponyms()))
st = firstLevel | secondLevel
st.add(root)
lst = list(st)

#build basic distance mat

mat = []
for syn_i in lst:
    matline = []
    for syn_j in lst:
        matline.append(syn_i.shortest_path_distance(syn_j))
    mat.append(matline)



secLvlLcsHypers = dict()
secLvlTraversed = set()
for i in secondLevel:
    for j in secondLevel:
        if i is not j and j not in secLvlTraversed:
            try:
                hyper = sorted(set(j.hypernyms()) & set(j.hypernyms()) & set(
                    firstLevel))[0]
            except:
                hyper = root
            secLvlLcsHypers[(i, j)] = hyper
    secLvlTraversed.add(i)

# calculate lin similarity
N = search_freq.sumFreqs()
def calcLin(c1, c2, l):
    def P(n):
        return n/N
    c1Freq = chooseFreq(c1)
    if c1Freq is None:
        return None
    c2Freq = chooseFreq(c2)
    if c2Freq is None:
        return None
    if l is None:
        try:
            lcs = secLvlLcsHypers[(c1,c2)]
        except:
            lcs = secLvlLcsHypers[(c2,c1)]
    else:
        lcs = l
    lcsFreq = chooseFreq(lcs)
    if lcsFreq is None:
        return None
    numerator = math.log(P(lcsFreq))*2
    denominator = math.log(P(c1Freq))+math.log(P(
        c2Freq))
    print(c1Freq, P(c1Freq), c2Freq, P(c2Freq), lcsFreq, P(lcsFreq))
    print(numerator,denominator)
    return numerator/denominator



linDict = dict()
for k in secLvlLcsHypers.keys():
    linDict[k] = calcLin(k[0],k[1], None)

secLvlTraversed = set()
for i in secondLevel:
    for j in firstLevel:
        if j in i.hypernyms():
            linDict[(i,j)] = calcLin(i,j,j)
        else:
            linDict[(i,j)] = calcLin(i,j,root)
    secLvlTraversed.add(i)

for w in st:
    linDict[(root,w)] = calcLin(w,root,root)

for c1,c2 in linDict.keys():
    try:
        v = linDict[(c1,c2)]
    except:
        v = linDict[(c2,c1)]
    print ((c1,c2), ':\t\t\t', v)
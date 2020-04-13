from nltk.corpus import wordnet as wn
import numpy as np

lst = []
bodyWaste = wn.synset('body_waste.n.01')
firstLevel = list(bodyWaste.hyponyms())
print(firstLevel)
for syn in firstLevel:
    lst.append(syn)
    lst = lst + list(syn.hyponyms())

mat = []
for syn_i in lst:
    matline = []
    for syn_j in lst:
        matline.append(syn_i.shortest_path_distance(syn_j))
    mat.append(matline)

for line in mat:
    print(line)
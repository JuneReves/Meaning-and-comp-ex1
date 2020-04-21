# Meaning and computation 2020, Huji. Ex.1, q.2.
# In order to find the required meaning of each synset (or choose a specific
# one) you should visit: http://wordnetweb.princeton.edu/perl/webwn and look
# for the word, and find the specific sense key.
# Built by June Reves


from syntree import *



#Get needed synsets form wordnet and list them = set()
root = wn.synset('furniture.n.01')
tree = synTree(Node(root, None, []))
LEVELS = 3

#extract tree:
def findChildren(syn):
    st = set()
    for n in tree.getNodes():
        st.union(n.getHyponyms())
    return set(syn.hyponyms()) - st


def extTree(syn, par, levels):
    if levels==0:
        return
    if syn is not root:
        node = Node(syn, par, [])
        tree.addNode(node)
        if par is tree.getRoot():
            tree.getRoot().addChild(node)
    else:
        node = tree.getRoot()
    for h in syn.hyponyms():
        extTree(h, node, levels-1)

extTree(root, None, LEVELS)

# Calculating the matrix
lst = sorted(tree.getNodes())
mat = []
for syn_i in lst:
    matline = []
    for syn_j in lst:
        matline.append(tree.LCAdistance(syn_j, syn_i))
    mat.append(matline)


# Printing the order of the synsets in the matrix (and the index)
for i in range(len(lst)):
    print(i+1, '\t', lst[i].getSynsetObj())

# Printing the matrix
for i in range(len(mat)):
    print(mat[i])

# Calculating the frequencies we need of all the synsets
tree.calcAllCumulativeFreqs()

print()

# calculating all available lin similarities and printing them
for i,j in tree.getAllPairs():
    sim = tree.findLinSimilarity(i,j)
    if sim is not None:
        print(j.getSynsetObj(), i.getSynsetObj())
        print('---------')
        print(tree.findLinSimilarity(i,j))
        print('---------')
        print()
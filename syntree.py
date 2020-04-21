from nltk.corpus import wordnet as wn
import search_freq
import math

d = search_freq.organizeData()
N = search_freq.sumFreqs()

class Node:
    __cumulativeFreq = None

    def __findFreq(self, syn):
        w = 0
        for word in syn.lemma_names():
            if search_freq.searchWordFreq(word, d) is not None:
                w += search_freq.searchWordFreq(word, d)
        return w

    def __init__(self, syn, parent, children):
        self.__parent = parent
        self.__syn = syn
        self.__children = children
        self.__words = sorted(self.__syn.lemma_names())
        self.__freq = self.__findFreq(syn)
        self.__hyponyms = self.__syn.hyponyms()
        self.__hypernyms = self.__syn.hypernyms()

    def getSynsetObj(self):
        return self.__syn

    def __lt__(self, other):
        return self.getWords()[0] < other

    def __gt__(self, other):
        return self.getWords()[0] > other

    def getWords(self):
        return self.__words
    def getHyponyms(self):
        return self.__hyponyms
    def getHypernyms(self):
        return self.__hypernyms
    def getParent(self):
        return self.__parent
    def getChildren(self):
        return self.__children

    def defCumulativeFreq(self, cumfreq):
        if self.__cumulativeFreq is not None:
            return False
        else:
            self.__cumulativeFreq = cumfreq

    def addChild(self, node):
        self.__children.append(node)

    def getFreq(self):
        return self.__freq

    def getCumulativeFreq(self):
        return self.__cumulativeFreq



class synTree:



    def __init__(self,root):
        self.__root = root
        self.__nodes = set()
        self.__nodes.add(root)
        self.__synsets = set()
        self.__synsets.add(root)
        self.__levels = [set()]
        self.__levels[0].add(root)


    def addNode(self, node):
        if node.getSynsetObj() in self.__synsets:
            return
        self.__nodes.add(node)
        self.__synsets.add(node.getSynsetObj())
        level = self.LCAdistance(node, self.__root)
        while len(self.__levels) <= level:
            self.__levels.append(set())
        self.__levels[level].add(node)

    def getRoot(self):
        return self.__root

    def getNodes(self):
        return self.__nodes

    def getSynsets(self):
        return self.__synsets

    def checkIfSynInTree(self, syn):
        return syn in self.__synsets


    def LCAdistance(self, c1, c2):
        lca = self.findLCA(c1,c2)
        return self.findAncsestorDistance(c1,lca) + \
               self.findAncsestorDistance(c2, lca)

    def findLCA(self, c1, c2):
        c1Ancestors = []
        cur = c1
        while cur is not None:
            c1Ancestors.append(cur)
            cur = cur.getParent()
        cur = c2
        counter = 0
        while cur is not None:
            for v in range(len(c1Ancestors)):
                if c1Ancestors[v] is cur:
                    return cur
            cur = cur.getParent()
        return None

    def findAncsestorDistance(self, node, anc):
        counter = 0
        cur = node
        while cur is not anc and cur is not None:
            counter += 1
            cur = cur.getParent()
        return counter

    def getNodeLevel(self, node):
        for l in self.__levels:
            if node in l:
                return l
        return None

    def getLevel(self, level):
        try:
            return self.__levels[level]
        except:
            return set()

    def calcCumulativeFreq(self, node):
        f = node.getFreq()
        for v in node.getChildren():
            try:
                f += self.calcCumulativeFreq(v)
            except:
                continue
        node.defCumulativeFreq(f)
        return f

    def calcAllCumulativeFreqs(self):
        self.calcCumulativeFreq(self.__root)

    def findLinSimilarity(self, c1, c2):
        def P(n):
            return n / N
        c1freq = c1.getCumulativeFreq()
        if c1freq == 0 or c1freq is None:
            return None
        c2freq = c2.getCumulativeFreq()
        if c2freq == 0 or c2freq is None:
            return None
        lcs = self.findLCA(c1,c2)
        lcsfreq = lcs.getCumulativeFreq()
        if lcsfreq is None:
            return None
        numerator = math.log(P(lcsfreq)) * 2
        denominator = math.log(P(c1freq)) + math.log(P(c2freq))
        return numerator / denominator

    def getAllPairs(self):
        pairs = set()
        iterated = set()
        for i in self.__nodes:
            for j in self.__nodes:
                if j in iterated or i is j:
                    continue
                pairs.add((i,j))
            iterated.add(i)
        return pairs
'''
Question 1:
-----------
The word 'hide':
A) Conceal, cover oneself (verb)
    I) "He hides the money."
    II) "They found the place where she hides in."
B) Pelt, skin (noun)
    I) "Rhinoceroses have thick hides covering their body"
    II) "Wearing deer hides for winter"
'''

with open('corpus_ex1', 'r') as corpus:

    lst_corpus = corpus.readlines()
    line = [l.strip() for l in lst_corpus]
    noise = ['<s>', '</s>']
    words = [w for w in line if w not in noise]
    words =  ''.join(str(words))

    from nltk.tokenize import sent_tokenize

    sentences = sent_tokenize(words)


    # Step one - taking all the sentences with 'will' in them
    hide_sent = []
    for sentence in sentences:
        if 'hide' in sentence:
            hide_sent.append(sentence)

    # for i in range(len(hide_sent)):
    #     print(hide_sent[i], '\n')


    # Step two -  sort them by sence A and sense B
'''
Sense A can be found mostly around function words, like 'in', 'behind' etc, pronouns and around 'the' as an accusative object.
Rougly speaking, we can match sentences with sense A based on these rules.

Sense B can be extracted by finding other hyponyms of 'animal' like 'deer' or find fords related to 'trade'/'commerce', or finding antonyms, like 'skin', like 'pelt'.   
'''
# Taking a few sentences for the training set in a context window of 2
'''
Sense A
--------

Found 6 sentences with 'hides' next to 'in', out of 61 occurrences (based on the corpus_freq), which points to sense A quite high (make it the threshold?) 
'''
function_words =['in', 'behind', 'to', 'I', 'he', 'you', 'she', 'it', 'we', 'they']
sense_A = []
sense_B = []




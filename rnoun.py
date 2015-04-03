def rnoun(x):
    nouns = []
    f = open('nounlist.txt', 'r')
    for i in f:
        nouns.append(i.strip())
    f.close()
    import random
    l = []
    for i in range(x):
        n = random.choice(nouns)
        if n in l:
            n = random.choice(nouns)
        l.append(n)
    for i in l:
        print i
        
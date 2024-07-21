omit = {'a','m','p','r','u','o','n','k'}
has = {'s','t'}

possible = []

with open("words.txt", "r") as f:
    for word in f:
        word = word.rstrip()
        wordSet = set(word)
        if (not bool(omit.intersection(wordSet)) and has.issubset(wordSet)):
            possible.append(word)

words = []

for word in possible:
    if (word[0] == 's' and word[1] == 't'):
        words.append(word)

print(words)
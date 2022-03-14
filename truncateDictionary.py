import re
import collections

with open("words.txt", 'r') as f:
    data = f.readlines()

truncDict = []
for word in data:
    if len(word[:-1]) == 5:
        if bool(re.search('^[a-z]*$', word[:-1])):
            if word[:3] == "spi":
                print(word, 2)
            truncDict.append(word[:-1])


'''
freq = collections.Counter("".join(truncDict))

for i in range(len(truncDict)):
    wordScore = 0
    for c in truncDict[i]:
        wordScore += freq[c]
    truncDict[i] = (truncDict[i], wordScore)

truncDict.sort(key=lambda x: x[1], reverse=True)

'''
print('######')
for i in range(len(truncDict)):
    if truncDict[i][:3] == "spi":
        print(truncDict[i])
    truncDict[i] = truncDict[i]+"\n"

with open("wordle_dictionary.txt", "w") as f:
    f.writelines(truncDict)


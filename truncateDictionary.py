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

print('######')
for i in range(len(truncDict)):
    if truncDict[i][:3] == "spi":
        print(truncDict[i])
    truncDict[i] = truncDict[i]+"\n"

with open("wordle_dictionary.txt", "w") as f:
    f.writelines(truncDict)


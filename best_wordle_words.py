import string
import re
import collections
import statistics
import matplotlib.pyplot as plt

#find the starting word that eliminates the most words on average

with open("wordle_dictionary.txt", 'r') as f:
    data = f.readlines()

def build_setDict(data):
    setDict = collections.defaultdict(set)
    LOWERCASE = string.ascii_lowercase
    for char in LOWERCASE:
        for pos in range(5):
            for word in data:
                if not char in word:
                    setDict[char + str(pos) + "0"].add(word)
                elif word[pos] != char:
                    setDict[char + str(pos) + "1"].add(word)
                else:
                    setDict[char + str(pos) + "2"].add(word)
    return setDict

setDict = build_setDict(data)

def char_join(guess, feedback):
    # guess: str
    # feedback: str
    # sets: defaultdict[set[str]]
    # rtype: set[str]
    res = setDict[guess[0] + "0" + feedback[0]]
    for i in range(1,5):
        res = res.intersection(setDict[guess[i] + str(i) + feedback[i]])
    return res

def int_2_ternary(n):
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))

    res = ''.join(reversed(nums))
    res = '0'*(5 - len(res)) + res
    return res

FEEDBACK = [int_2_ternary(i) for i in range(244)]

def rank_words(word):
    res = []
    mn, mx = float('inf'),-1 
    for fb in FEEDBACK:
        ret = char_join(word, fb)
        subsetLen = len(ret)
        if subsetLen > 0:
            res.append(subsetLen)
        if subsetLen >= 2 and subsetLen < mn:
            mn = subsetLen
        if subsetLen > mx:
            mx = subsetLen

    return statistics.mean(res), statistics.stdev(res), mn, mx
        
def hist_word(word):
    res = []
    for i in range(244):
        feedback = int_2_ternary(i)
        ret = char_join(word, feedback, setDict)
        subsetLen = len(ret)
        if subsetLen > 0:
            res.append(subsetLen)

    plt.hist(res, 20)
    plt.show()

def word_subset_distribs():
    res = []
    for word in data:
        mu, stdv, mn, mx = rank_words(word)
        plt.plot(mu, stdv,"+")
        res.append([word, mu, stdv, mn, mx])
        print(word)
    plt.show()

    res.sort(key=lambda x: x[2])

    print("\tWord\t|\tMeanSubsetLen\t|\tStDev\t|\tMin\t|\tMax")
    print("-"*80)
    for i in range(50):
        print(f'\t{res[i][0][:-1]}\t|\t{round(res[i][1], 2)}\t\t|\t{round(res[i][2], 2)}\t|\t{round(res[i][3])}\t|\t{round(res[i][4])}') 

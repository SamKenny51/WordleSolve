import string
import re
import collections
import statistics
import matplotlib.pyplot as plt
import copy
import time
from pytrends.request import TrendReq

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
    guess = [c for c in guess]
    feedback = [c for c in feedback]
    gf = [(g, f, i) for g, f, i in zip(guess, feedback, ['0','1','2','3','4'])]
    gf.sort(reverse=True, key=lambda x: int(x[1]))
    res = copy.copy(setDict[gf[0][0] + gf[0][2] + gf[0][1]])
    for i in range(1,5):
        if (res.intersection(setDict[gf[i][0] + gf[i][2] + gf[i][1]])):
            res = res.intersection(setDict[gf[i][0] + gf[i][2] + gf[i][1]])
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

class revertableSet:
    def __init__(self, guess, feedback):
        self.results = [char_join(guess, feedback)]
        self.sampleDict = None

    def intersectCharJoin(self, guess, feedback):
        self.results.append(self.results[-1].intersection(char_join(guess, feedback)))

    def revert(self):
        if len(self.results) > 1:
            self.results.pop()

    def recommend(self):
        sample = list(self.results[-1])
        if not self.sampleDict:
            self.sampleDict = []
            pytrend = TrendReq()
            for i in range(0, len(sample), 5):
                if i+5 < len(sample):
                    r = sample[i:i+5]
                else:
                    r = sample[i:len(sample)]
                pytrend.build_payload(kw_list=r, timeframe='today 3-m')
                df = pytrend.interest_over_time()
                for j in range(len(r)):
                    self.sampleDict.append([r[j],df.iloc[-2,j]])
                time.sleep(0.01)

            self.sampleDict.sort(key=lambda x: x[1])
            
        else:
            while not (self.sampleDict[-1][0] in sample):
                self.sampleDict.pop()

        return self.sampleDict[-1][0]
    
    def __str__(self):
        return ''.join(list(self.results[-1]))

    def __len__(self):
        return len(self.results[-1])

def play_wordle(startingWord, feedback):
    res = revertableSet(startingWord, feedback)
    i = 0
    while len(res) > 1 and i < 6:
        print(f'{len(res)} words remaining.')
        print(res)
        newWord = res.recommend()
        print(f'New word is \'{newWord[:-1]}\'. Enter feedback.')
        feedback = input()
        res.intersectCharJoin(newWord[:-1], feedback)
        i += 1
    print(res)

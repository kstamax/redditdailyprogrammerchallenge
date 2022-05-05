from typing import final
import requests as req
wordsurl = 'https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt'
words = str(req.get(wordsurl).content).replace("b'","").replace("'","").split('\\n')
def unique(l):
    '''Returns list with unique values'''
    res = []
    for e in l:
        if not(e in res):
            res.append(e)
    return res
def lettersum(s):
    res = 0
    for l in s:
        res += (ord(l)-96)
    return res
def task1():
    for word in words:
        if lettersum(word) == 319:
            return word
def task2():
    wc = 0
    for word in words:
        if lettersum(word)%2!=0:
            wc+=1
    return wc
def task3():
    lettersumlist = [lettersum(x) for x in words]
    u_lettersumlist = unique(lettersumlist)
    cDict = {}
    for i in u_lettersumlist:
        cDict[i] = lettersumlist.count(i)
    return max(cDict, key=cDict.get)
def task4():
    res = {}
    lettersumlist = [lettersum(x) for x in words]
    u_lettersumlist = unique(lettersumlist)
    wordsDict = {}
    for i in u_lettersumlist:
        wordsDict[i] = [x for n,x in zip(lettersumlist,words) if n == i]
    for k in wordsDict:
        l = wordsDict[k]
        for i in range(len(l)-1):
            for j in range(i,len(l)):
                if abs(len(l[i])-len(l[j])) == 11:
                    if not (l[i] in res):
                        res[l[i]] = [l[j]]
                    else:
                        res[l[i]].append(l[j])
    return res
def task5():
    res = {}
    lettersumlist = [lettersum(x) for x in words]
    u_lettersumlist = unique(lettersumlist)
    wordsDict = {}
    for i in [x for x in u_lettersumlist if x > 188]:
        wordsDict[i] = [x for n,x in zip(lettersumlist,words) if n == i]
    for k in wordsDict:
        l = wordsDict[k]
        for i in range(len(l)-1):
            for j in range(i,len(l)):
                letters_in_common = False
                for c in l[i]:
                    if c in l[j]:
                        letters_in_common = True
                        break
                if not letters_in_common:
                    if not (l[i] in res):
                        res[l[i]] = [l[j]]
                    else:
                        res[l[i]].append(l[j])
    return res  
def task6():
    final_res = []
    res = []
    lettersumlist = [lettersum(x) for x in words]
    len_words = [len(x) for x in words]
    u_len_words = sorted(unique(len_words),reverse=True)
    wordsDict = {}
    words_zipped = list(zip(len_words,lettersumlist, words))
    for i in u_len_words:
        wordsDict[i] = [(z,y,x) for z,y,x in words_zipped if z == i]
    for i in wordsDict:
        wordsDict[i] = sorted(wordsDict[i],key = lambda x:x[0])
    for r in range(len(wordsDict)):
        cur_list = []
        prev_lettersum = 0
        for i in range(r,len(wordsDict)):
            for j in wordsDict[list(wordsDict.keys())[i]]:
                if j[1] > prev_lettersum:
                    prev_lettersum = j[1]
                    cur_list.append(j)
                    break
        res.append(cur_list)
    maxLength = max([len(x) for x in res])
    for r in res:
        if len(r) == maxLength:
            final_res.append(r)

    return final_res
desc = 'Options:\n0-Close the program;\n1-Word with letter sum of 319;\n2-Number of words with odd lettersum;\n3-Most common lettersum;\n4-Pair of words with the same letter sum whose lengths differ by 11 letters;\n5-Pair of words that have no letters in common, and that have the same letter sum, which is larger than 188;\n6-The longest list where each word has both a different number of letters, and a different letter sum.\n The list is sorted both in descending order of word length, and ascending order of letter sum;\n7-Lettersum of word;'
print(desc)
while True:
    p = input('Select option (type "options" to see list of options): ')
    if p == "0":
        break
    elif p == "1":
        print(task1())
    elif p == "2":
        print(task2())
    elif p == "3":
        print(task3())
    elif p == "4":
        print(task4())
    elif p == "5":
        print(task5())
    elif p == "6":
        print(task6())
    elif p == "7":
        while True:
            s = input('Enter word or "0" to return back: ')
            if s == "0":
                break
            print(f'lettersum: {lettersum(s)}')
    elif p == "options":
        print(desc)
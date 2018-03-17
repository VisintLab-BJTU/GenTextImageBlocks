# -*- coding: utf-8 -*-
# vim:fenc=utf-8

words = {}
with open("../words.txt") as f:
    text = f.read()
    text=text.replace(' ','').replace('\n','').replace('\r','')
    print len(text)
    text = unicode(text, 'utf-8')
    for word in text:
        if word not in words:
            words[word] =0
        words[word] = words[word] + 1

print len(words)
x = [(words[x], x) for x in words]
print len(x)
x = sorted(x)
_map = []
with open ('../freq.txt', 'w') as f:
    for cnt, word in x:
        if word == '\n' or word == '\r':
            print 'yes!'       
        _map.append(word)
        #f.write(word.encode('utf-8') + " " + str(cnt) + "\n")

_map.sort()

with open ('../map.txt', 'w') as f:
    ind = 1
    for word in _map:
        f.write(str(ind) + " " + word.encode('utf-8') + "\n")
        ind = ind + 1

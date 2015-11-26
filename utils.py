#useful research functions

import datetime

def out(l):
    #print nicely the list l
    for i,x in enumerate(l):
        print str(i) + ": " + str(x)

def histogram(l):
    #create the histogram of the list l (returns dict)
    d = {}
    for x in l:
        d[x] = d.get(x, 0) + 1
    return d

def dateParser(date_string):
## Input: String of e-mail metadata data
## Output: date object
    f = "%a, %d %b %Y %H:%M:%S"
#    f = "%a, %d %b %Y %H:%M:%S"
    return datetime.datetime.strptime(" ".join(date_string.split()[0:5]), f)
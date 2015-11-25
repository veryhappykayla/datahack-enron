#useful research functions

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

          

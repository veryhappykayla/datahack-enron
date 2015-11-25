### connections ####

## imports ##
import networkx as nx
import pylab
import pickle
from initial_data_parser import *

class Connection(object):
    def __init__(self, A, B, n_times = 0): # n_times is how many times A sent B a massege
            self.graph = nx.Graph()
            self.sender = A
            self.reciver = B
            self.n_times = n_times
            self.ID = str(hash(A))+str(hash(B)) # for checking if there more than one connection between 2 people 

    def inc(self):
        self.n_times += 1

    def get_ID(self):
        return self.ID


#### Manipulating Data ####

def build_graph(mails): #need to get persons from guy
    ALL_CONNECTIONS = {}
    G = nx.DiGraph()
    for mail in mails:
        new_connection = Connection(mail.headers['To'], mail.headers['From'])
        if ALL_CONNECTIONS.has_key(new_connection.get_ID()):
            ALL_CONNECTIONS[new_connection.get_ID()].inc()
        else:
            ALL_CONNECTIONS[new_connection.get_ID()] = new_connection
            
    for val in ALL_CONNECTIONS.values():
        G.add_edge(val.sender, val.reciver, weight = val.n_times)
    return G


#########################
## helpful functions ####
#########################
def print_graph(G):
    #TODO
    # need to print lables on the red dots
    nx.draw(G)
    pylab.show()

def out(lst):
    for i in range(len(lst)):
        print str(i) + " :" + lst[i]

#Testing
        
#a = pickle.load(file('./sample.pickle'))
#mails = [a[0].folders_list[0][i] for i in range(628)]
        
     

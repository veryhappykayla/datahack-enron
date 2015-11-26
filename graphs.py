### connections ####

## imports ##
import networkx as nx
import pylab
import pickle
from initial_data_parser import *
import math

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

###########################
#### Manipulating Data ####
###########################

def give_key_by_val(D, address):
    for item in D:
        if address in D[item]:
            return item
    return None

def build_graph(mails, start_date = None, end_date = None):
    D = load_person_dict(file('./persons.json'))
    ALL_CONNECTIONS = {}
    G = nx.DiGraph()
    #filtering mails by time
    if start_date != None and end_date != None: 
        for mail in mails:
            if (mail.headers['Date'] < start_date) or (mail.headers['Date'] > end_date):
               mails.remove(mail) 
    #combining all mail to graph
    for mail in mails:
        addresses = parse_address(mail.headers['To'])
        for add in addresses:
            if (give_key_by_val(D, add) != None) and (give_key_by_val(D, mail.headers['From']) != None):
                new_connection = Connection(give_key_by_val(D, add), give_key_by_val(D, mail.headers['From']))
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

def parse_address(address):
    if address == None:
        return []
    return [x.replace('\r\n', '') for x in address.split(',')]


'''      
a = pickle.load(file('../sample.pickle'))
mails = [a[0].folders_list[0][i] for i in range(628)]
'''
     

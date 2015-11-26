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
    
def build_graph(mails, start_date = None, end_date = None):
    ALL_CONNECTIONS = {}
    G = nx.DiGraph()
    #filtering mails by time
    if start_date != None and end_date != None: 
        for mail in mails:
            if (mail.headers['Date'] < start_date) or (mail.headers['Date'] > end_date):
               mails.remove(mail) 
    #combining all mail to graph
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

def get_unique_list(lst):
    ret_lst = []
    for i in lst:
        if i in ret_lst:
            pass
        else:
            ret_lst.append(i)
    return ret_lst

def parse_address(address):
    if address == None:
        return []
    return [x.replace('\r\n', '') for x in address.split(',')]

def pkod_mail(lst): # lst is a list of name and list of adresses
    ret_dict = {}
    for i in lst:
        for j in i[1]: #there are several adresses in each mail
            if ret_dict.has_key(j):
                ret_dict[j] += 1
            else:
                ret_dict[j] = 1
    return ret_dict

def average(lst): #lst is a lst of ints
    return sum(lst)/(len(lst)*1.0)

def norm(lst): #lst is a lst of ints - returns norm of vector
    av = average(lst)
    total = 0
    for i in lst:
        total += (i - av)*(i - av)
    return (math.sqrt(total) / (av*1.0))

def map_person_to_mails(person):
    name = person.name
    possible_mails = []
    for folder in person.get_folder_list():
        if (folder.name == "inbox") and len(folder.emails_list)!= 0: #for sent mails we would like to look at the from field and not on the To
            email_list = [(folder.emails_list[x].get_name(), parse_address(folder.emails_list[x].get_headers()['To']))\
                          for x in range(len(folder.emails_list))] 
            M = pkod_mail(email_list)
            if M.values() != []:
                n = norm(M.values())
                for i in M:
                    if M[i] > n + 5: # 5 is magic number
                        possible_mails.append(i)
        if "sent" in folder.name and len(folder.emails_list)!= 0:
            email_list = [(folder.emails_list[x].get_name(), parse_address(folder.emails_list[x].get_headers()['From']))\
                          for x in range(len(folder.emails_list))]
            M = pkod_mail(email_list)
            n = norm(M.values())
            for i in M:
                if M[i] > n + 5: # 5 is magic number
                    possible_mails.append(i)
    return get_unique_list(possible_mails)
            

#Testing

'''      
a = pickle.load(file('../sample.pickle'))
mails = [a[0].folders_list[0][i] for i in range(628)]
'''
     
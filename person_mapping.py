####################
## Person mapping ##
####################

import pickle
from initial_data_parser import *
import math
import json

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
    return (name, get_unique_list(possible_mails))

def load_person_dict(fp = file('./persons.json')):
    return json.load(fp)




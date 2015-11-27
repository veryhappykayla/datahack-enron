##################
## Productivity ##
##################

#### Imports ####
import pickle
from initial_data_parser import *
import math
import json
from person_mapping import *
import datetime
from count_emails import *

MAIL_TYPES = {"FUN": -1, "WORK": 1, "TECHNICAL": 0.5, "QUESTION": 0, "POLITICS": 0}
# I assume that mails are classified as Fun or Work

'''
a = pickle.load(file('../sent_1.pickle'))
cla = pickle.load(file('./mail_classification.pickle'))
topics = json.load(file('./lda/topic_categorization.txt', 'rb'))
D = load_person_dict(file('./persons.json'))
'''

def give_productive_score_to_week(Person, start_date, cla):
    mails = Person.get_all_emails()
    mails = sort_mails(mails)
    classification = cla[Person.get_name()]
    new_classification = []
    for c in classification:
        new_classification.append((c[0].split('/')[-1], c[-1]))
    new_classification = dict(new_classification)
    
    mails_by_day = []
    for d in range(7):
        mails_by_day.append(get_mail_by_day(start_date + datetime.timedelta(d), mails))

    results = []
    for day in range(7):
        day_score = [0, 0, 0] # WORK / FUN / UNKNOWN
        
        for m in mails_by_day[day][1]:
            if new_classification[m.get_name()] == "Work":
                day_score[0] += 1
            elif new_classification[m.get_name()] == "Fun":
                day_score[1] += 1
            else:
                day_score[2] += 1
             # maybe Fun is (-1) and Work is 1
        results.append(day_score)
    return results

def give_productive_score_to_mails(person, mails, cla):
    classification = cla[person.get_name()]
    new_classification = []
    for c in classification:
        new_classification.append((c[0].split('/')[-1], c[-1]))
    new_classification = dict(new_classification)
    score = [0, 0, 0]
    for m in mails:
            if new_classification[m.get_name()] == "Work":
                score[0] += 1
            elif new_classification[m.get_name()] == "Fun":
                score[1] += 1
            else:
                score[2] += 1
    return score

#### running line


spammers = ['sanders-r', 'fossum-d', 'nemec-g', 'arnold-j', 'perlingiere-d', 'love-p', 'taylor-m', 'scott-s', 'symes-k', 'beck-s', 'lenhart-m', 'bass-e', 'jones-t', 'shackleton-s', 'germany-c', 'dasovich-j', 'kaminski-v', 'mann-k']
#i=2;week = group_mails_by_week(a[i].get_all_emails());[give_productive_score_to_mails(a[i], week[x][-1], cla) for x in range(len(week))]

### TODO ####
## ------ ###
#
# 1) is productivity relevant just for an individual person or for a group of persons?
# 2) need to think of a way that will consider the number of mails the user sent in a week
# 3) 
    
    

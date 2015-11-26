import utils
import pickle
from initial_data_parser import *
import math
import json
from person_mapping import *

def is_sent_by_user(Person, mail, person_dictionay):
    name = Person.name
    relevant_emails = person_dictionay[name]
    if mail.headers['From'] in relevant_emails:
        return True
    return False
    

def filter_mail_for_user_by_time(Person, start_date, end_date, person_dictionay):
        name = Person.name
        relevant_emails = person_dictionay[name]
        new_mails = []
        for mail in Person.get_all_emails():
            if mail.headers['From'] in relevant_emails:
                new_mails.append(mail)
	# check if the time fits
        if start_date != None and end_date != None:
            for main in new_mails:
                if  start_date < mail.headers['Date'] < end_date:
                    pass
                else:
                    new_mails.remove(mail)
        return new_mails

def group_mails_by_week(mails):
    mails = sorted(mails, key = lambda x: utils.dateParser(x.headers['Date']).toordinal())
    start_date = utils.dateParser(mails[0].headers['Date']).isocalendar()
    
    ret_list = []
    current_year = start_date[0]
    current_week = start_date[1]
    new_mails = []
    for mail in mails:
        iso_date = utils.dateParser(mail.headers['Date']).isocalendar()
        if iso_date[0] == current_year and iso_date[1] == current_week:
            new_mails.append(mail)
        else:
            ret_list.append((current_year, current_week, new_mails))
            new_mails = []
            if current_week == 51:
                current_week = 0
                current_year += 1
            else:
                current_week += 1
    return ret_list
            

WEEK_DAYS = {7:'Sun' , 1: 'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5 : 'Fri', 6: 'Sat'}

def get_relevant_mails_from_user(Person, person_dictionay):
    relevant_adresses = person_dictionay[Person.get_name()]
    ret_mails = []
    for mail in Person.get_all_emails():
        if mail.headers['From'] in relevant_adresses:
            ret_mails.append(mail)
    return ret_mails

def count_mails_in_day(mails, day, WEEK_DAY_dict = WEEK_DAYS): # day is a value of WEEK_DAYS
    count = 0
    for mail in mails:
        if WEEK_DAY_dict[utils.dateParser(mail.headers['Date']).isoweekday()] == day:
            count += 1
    return count

def count_for_each_day(mails):
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    return [count_mails_in_day(mails, day) for day in days]

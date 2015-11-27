import utils
import pickle
from initial_data_parser import *
import math
import json
from person_mapping import *
import datetime

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

#need to fix this function
def group_mails_by_week(mails):
    mails = sorted(mails, key = lambda x: utils.dateParser(x.headers['Date']).toordinal())
    start_date = utils.dateParser(mails[0].headers['Date']).isocalendar()
    
    ret_list = []
    current_year = start_date[0]
    current_week = start_date[1]
    new_mails = []
    for i in range(len(mails)):
        iso_date = utils.dateParser(mails[i].headers['Date']).isocalendar()
        if iso_date[0] == current_year and iso_date[1] == current_week:
            new_mails.append(mails[i])
        else:
            ret_list.append((current_year, current_week, new_mails))
            new_mails = []
            if current_week == 53:
                current_week = 1
                current_year += 1
            else:
                current_week += 1
            i -= 1
    return ret_list

def sort_mails(mails):
    return sorted(mails, key = lambda x: utils.dateParser(x.headers['Date']).toordinal())

def get_mail_by_day(date, mails):
    ret_list = []
    found_one = False
    year, month, day = date.year, date.month, date.day
    for i in range(len(mails)):
        mail_date = utils.dateParser(mails[i].headers['Date'])
        if mail_date.year == year and mail_date.month == month and mail_date.day == day:
            ret_list.append(mails[i])
            found_one = True
        else:
            if found_one == True:
                return (i ,ret_list)
    if found_one:
        return (i, ret_list)
    return (0, ret_list)

def get_all_mails_for_all_days(mails):
    mails = sort_mails(mails)
    for i in range(len(mails)):
        if utils.dateParser(mails[i].headers['Date']).year < 1998:
            pass
        else:
            mails = mails[i:]
            break
    first_date = utils.dateParser(mails[0].headers['Date'])
    last_date = utils.dateParser(mails[-1].headers['Date'])
    ret_list = []
    index = 0
    
    for d in range((last_date - first_date).days):
        current_date = first_date + datetime.timedelta(d)
        new_index, mm = get_mail_by_day(current_date, mails[index:])
        index += new_index
        #print index
        ret_list.append((current_date, mm))
    return ret_list

def get_all_mails_for_all_days_for_user(user):
    mails = user.get_all_emails()
    return get_all_mails_for_all_days(mails)
    
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

def filter_by_hour(mails, hour): # day is a value of WEEK_DAYS
    ret_mail = []
    for mail in mails:
        if utils.dateParser(mail.headers['Date']).hour == hour:
            ret_mail.append(mail)
    return ret_mail

def get_mails_by_day(mails, day, WEEK_DAY_dict = WEEK_DAYS):
    ret_mails = []
    for mail in mails:
        if WEEK_DAY_dict[utils.dateParser(mail.headers['Date']).isoweekday()] == day:
            ret_mails.append(mail)
    return ret_mails

def count_for_each_day(mails):
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    return [count_mails_in_day(mails, day) for day in days]

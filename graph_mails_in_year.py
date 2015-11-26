# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pylab
import pickle

def load_data_from_pickle(data_path):
    return pickle.load(file(data_path))
    
  

  
def get_sending_time(sender):
    all_data = load_data_from_pickle(data_path)
    person = ------
    all_mails = person.get_all_emails()
    mails_by_date = {}
    for mail in all_mails:
        if #to check if he is the sender
            mail_date = data_parser(mail.get_headers('date'))
            if mail_date in mails_by_data:
                mails_by_date[mail_date] += 1
            else:
                mails_by_date[mail_date] = 1
        

            
        
        
    

def sending_mails_year(person):
    times = get_sending_time(person)
    count_mails = get_mails_per_day(sender)
    plt.plot(times,count_mails, 'ro')
    plt.axis()

    return plt.show()
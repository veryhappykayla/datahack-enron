from email.parser import Parser
import glob
import os
import json
import pickle
import base64

######################
### STATIC GLOBALS ###
######################

def load_person_dict(fp = file('./persons.json')):
    res = json.load(fp)
    fp.close()
    return res

def load_topic_dict(fp = file('./lda/topic_categorization.txt')):
    res = json.load(fp)
    fp.close()
    return res

def reverse_dict(d):
    new_d = {}
    for x,y in d.iteritems():
        for z in y:
            new_d[z] = new_d.get(z, ()) + (x,)
    return new_d

PERSON_DICT = load_person_dict()
TOPIC_DICT = load_topic_dict()
REV_TOPIC_DICT = reverse_dict(TOPIC_DICT)

#########################
### PARSING FUNCTIONS ###
#########################


def parse_email_headers(email_data):
    headers = Parser().parsestr(email_data)
    return headers

def parse_email_content(email_data):
    content_start = email_data.find('\r\n\r\n') + 4
    return email_data[content_start:]

def dateParser(date_string):
## Input: String of e-mail metadata data
## Output: date object
    f = "%a, %d %b %Y %H:%M:%S"
#    f = "%a, %d %b %Y %H:%M:%S"
    return datetime.datetime.strptime(" ".join(date_string.split()[0:5]), f)

def dump_email_to_file(email, dir_path = "C:\\Users\\Guy\\Desktop\\datahack\\sent_mails_with_content\\"):
    owner_name = email.get_owner().get_name()
    file_name = (email.get_folder_name() + "/" + email.get_name()).replace("/","#")
    #print dir_path + owner_name + "_" + file_name + "_" + base64.b64encode(email.get_headers()['Date'])
    file(dir_path + owner_name + "_" + file_name + "_" + base64.b64encode(email.get_headers()['Date']), 'wb').write(email.get_content())
	
def parse_filename_to_data(filename):
    filename = filename.split("/")[-1]
    filename = filename.split("\\")[-1]
    splited = filename.split("_")
    owner_name, email_path, date = splited[0], '_'.join(splited[1:-1]).replace("%23","/"), splited[-1]
    date = base64.b64decode(date)
    return owner_name, email_path, date
        
def parse_threshabs_to_users(file_path, num_of_topics = 10):
    data = [x.strip().split('\t') for x in file(file_path,'rb').readlines()]
    data = data[1:]
    meta_data = [parse_filename_to_data(x[1]) for x in data]
    data = [map(float,x[2:]) for x in data]
    total_num_of_topics = len(data[0])
    res = {}
    counter = 0
    for email_meta_data, email_data in zip(meta_data, data):
        counter += 1
        curr_data = res.get(email_meta_data[0], [0 for i in xrange(total_num_of_topics)])
        res[email_meta_data[0]] = [x+y for x,y in zip(curr_data, email_data)]
        if not counter % 1000:
            print counter

    final_res = []
    for owner_name, user_data in res.iteritems():
        strongest_indices = sorted(enumerate(user_data), key = lambda x: -x[1])[:10]
        sum_probs = sum([x[1] for x in strongest_indices])
        strongest_indices = [(x[0],x[1]/sum_probs) for x in strongest_indices]
        final_res.append((owner_name, strongest_indices))
    return final_res

def parse_threshabs_to_users_by_emails(file_path):
    data = [x.strip().split('\t') for x in file(file_path,'rb').readlines()]
    data = data[1:]
    meta_data = [parse_filename_to_data(x[1]) for x in data]
    data = [map(float,x[2:]) for x in data]
    total_num_of_topics = len(data[0])
    res = {}
    counter = 0
    for email_meta_data, email_data in zip(meta_data, data):
        counter += 1
        owner_name, email_path, date = email_meta_data
        curr_l = res.setdefault(owner_name, [])
        res[owner_name].append((email_path, date, label_email_topic(email_data)))
        if not counter % 1000:
            print counter

    return res

def parse_threshabs_to_politics(file_path):
    data = [x.strip().split('\t') for x in file(file_path,'rb').readlines()]
    data = data[1:]
    meta_data = [parse_filename_to_data(x[1]) for x in data]
    data = [map(float,x[2:]) for x in data]
    total_num_of_topics = len(data[0])
    res = {}
    counter = 0
    for email_meta_data, email_data in zip(meta_data, data):
        counter += 1
        owner_name, email_path, date = email_meta_data
        curr_l = res.setdefault(owner_name, [])
        res[owner_name].append((email_path, date, is_politics_email(email_data)))
        if not counter % 1000:
            print counter

    return res

def is_politics_email(email_data):
    return email_data[34] > 0.3
    #"C:\Users\Guy\Desktop\datahack\enron_mail_20150507\maildir\jones-t\sent\2442"

def label_email_topic(email_data):
    #email_data is a list of weights, each one corresponding to a topic.
    label_strength = {}
    for i,f in enumerate(email_data):
        for label in REV_TOPIC_DICT[i]:
            label_strength[label] = label_strength.get(label, 0) + f
    return sorted(label_strength.items(), key = lambda x: -x[1])[0][0]
        
def HACK_label_email_topic(email_data):
    #email_data is a list of weights, each one corresponding to a topic.
    label_strength = {}
    for i,f in email_data:
        for label in REV_TOPIC_DICT[i]:
            label_strength[label] = label_strength.get(label, 0) + f
    return sorted(label_strength.items(), key = lambda x: -x[1])

###############
### OBJECTS ###
###############

class Email(object):
    def __init__(self, email_path, folder_name, owner, with_content = False):
        email_data = file(email_path, 'rb').read()
        self.headers = parse_email_headers(email_data)
        self.name = email_path.split('\\')[-1]
        self.owner = owner
        self.folder_name = folder_name
        if with_content:
            self.content = parse_email_content(email_data)
        else:
            self.content = None

    def get_headers(self):
        return self.headers

    def get_name(self):
        return self.name

    def get_folder_name(self):
        return self.folder_name

    def get_owner(self):
        return self.owner

    def get_content(self):
        try:
            return self.content
        except: #backwards compatibility with old pickle
            return None

    def is_sent_by_owner(self, person_dictionay = PERSON_DICT):
        owner_name = self.get_owner().get_name()
        relevant_emails = person_dictionay[owner_name]
        if self.get_headers()['From'] in relevant_emails:
            return True
        return False

class Folder(object):
    def __init__(self, folder_path, parent_name, owner, with_content = False, only_sent_by = True):
        if parent_name == "":
            self.name = folder_path.split('\\')[-1]
        else:
            self.name = parent_name + "/" + folder_path.split('\\')[-1]
        self.owner = owner
        
        all_paths = glob.glob(folder_path + "/*")
        if only_sent_by:
            all_paths = [p for p in all_paths if "sent" in p]
        #parse emails
        email_paths = [x for x in all_paths if os.path.isfile(x)]
        self.emails_list = [Email(email_path, self.name, self.owner, with_content) for email_path in email_paths]
        if only_sent_by:
            self.emails_list = [x for x in self.emails_list if x.is_sent_by_owner()]
        #parse inner folders
        inner_folders_paths = [x for x in all_paths if not os.path.isfile(x)]
        self.inner_folders_list = [Folder(inner_folders_path, self.name, owner, with_content, only_sent_by) for inner_folders_path in inner_folders_paths]
        self.full_list = self.inner_folders_list + self.emails_list

    def get_owner(self):
        return self.owner
    
    def get_name(self):
        return self.name

    def get_email_list(self):
        return self.emails_list

    def get_all_emails(self):
        mails_in_folder = self.get_email_list()
        for inner_folder in self.get_inner_folders_list():
            mails_in_folder.extend(inner_folder.get_all_emails())
        return mails_in_folder
    
    def get_inner_folders_list(self):
        return self.inner_folders_list
    
    def __iter__(self):
        return iter(self.full_list)
    def __getitem__(self, val):
        return self.full_list.__getitem__(val)
    def __len__(self):
        return len(self.full_list)


class Person(object):
    def __init__(self, person_path, with_content = False, only_sent_by = True):
        print "Creating " + person_path.split('\\')[-1] + "...",
        self.name = person_path.split('\\')[-1]
        folder_paths = glob.glob(person_path + "/*")
        self.folders_list = [Folder(folder_path, "", self, with_content, only_sent_by) for folder_path in folder_paths]
        print "Done, with %d mails" % len(self.get_all_emails())

    def get_name(self):
        return self.name

    def get_folder_list(self):
        return self.folders_list

    def get_all_emails(self):
        all_emails = []
        for folder in self:
            all_emails.extend(folder.get_all_emails())
        return all_emails

    def __iter__(self):
        return iter(self.folders_list)

    def __getitem__(self, val):
        return self.folders_list.__getitem__(val)

    def __len__(self):
        return len(self.folders_list)

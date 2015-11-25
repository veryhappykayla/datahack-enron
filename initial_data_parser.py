from email.parser import Parser
import glob
import os

#########################
### PARSING FUNCTIONS ###
#########################


def parse_email_headers(email_data):
    headers = Parser().parsestr(email_data)
    return headers

###############
### OBJECTS ###
###############

class Email(object):
    def __init__(self, email_path):
        email_data = file(email_path, 'rb').read()
        self.headers = parse_email_headers(email_data)
        self.name = email_path.split('\\')[-1]

    def get_headers(self):
        return self.headers

    def get_name(self):
        return self.name

    
class Folder(object):
    def __init__(self, folder_path):
        email_paths = glob.glob(folder_path + "/*")
        self.emails_list = [Email(email_path) for email_path in email_paths]
        self.name = folder_path.split('\\')[-1]

    def get_name(self):
        return self.name

    def get_email_list(self):
        return self.emails_list

    def __iter__(self):
        return iter(self.emails_list)
    def __getitem__(self, val):
        return self.emails_list.__getitem__(val)
    def __len__(self):
        return len(self.emails_list)



class Person(object):
    def __init__(self, person_path):
        print "Creating " + person_path.split('\\')[-1] + "..."
        folder_paths = glob.glob(person_path + "/*")
        self.folders_list = [Folder(folder_path) for folder_path in folder_paths]
        self.name = person_path.split('\\')[-1]

    def get_name(self):
        return self.name

    def get_folder_list(self):
        return self.folders_list

    def __iter__(self):
        return iter(self.folders_list)
    def __getitem__(self, val):
        return self.folders_list.__getitem__(val)
    def __len__(self):
        return len(self.folders_list)

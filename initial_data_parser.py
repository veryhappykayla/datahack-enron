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
    def __init__(self, email_path, folder_name, owner):
        email_data = file(email_path, 'rb').read()
        self.headers = parse_email_headers(email_data)
        self.name = email_path.split('\\')[-1]
        self.owner = owner
        self.folder_name = folder_name

    def get_headers(self):
        return self.headers

    def get_name(self):
        return self.name

    def get_folder_name(self):
        return self.folder_name

    def get_owner(self):
        return self.owner

    
class Folder(object):
    def __init__(self, folder_path, parent_name, owner):
        if parent_name == "":
            self.name = folder_path.split('\\')[-1]
        else:
            self.name = parent_name + "/" + folder_path.split('\\')[-1]
        self.owner = owner
        
        all_paths = glob.glob(folder_path + "/*")
        #parse emails
        email_paths = [x for x in all_paths if os.path.isfile(x)]
        self.emails_list = [Email(email_path, self.name, self.owner) for email_path in email_paths]
        #parse inner folders
        inner_folders_paths = [x for x in all_paths if not os.path.isfile(x)]
        self.inner_folders_list = [Folder(inner_folders_path, self.name, owner) for inner_folders_path in inner_folders_paths]
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
    def __init__(self, person_path):
        print "Creating " + person_path.split('\\')[-1] + "..."
        folder_paths = glob.glob(person_path + "/*")
        self.folders_list = [Folder(folder_path, "", self) for folder_path in folder_paths]
        self.name = person_path.split('\\')[-1]

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

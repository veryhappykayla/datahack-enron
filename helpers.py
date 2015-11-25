import datetime

def dateParser(date_string):
## Input: String of e-mail metadata data
## Output: date object
    f = "%a, %d %b %Y %H:%M:%S"
#    f = "%a, %d %b %Y %H:%M:%S"
    return datetime.datetime.strptime(" ".join(date_string.split()[0:5]), f)
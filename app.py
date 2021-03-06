import re
import json
import appbackend
from time import strptime

counter = 0

# tuple that holds items that will be mapped as keys in dictionary
list_categories = ('date', 'time', 'sourceIP', 'destinationIP', 'sourcePort', 'destinationPort')

# Pattern Order:
# Date, Time, Source IP, Destination IP, Source Port, Destination Port
# regex pattern that extracts data from log file
patterns = [r'^[A-Z][a-z]*\s\d*', r'[0-9][0-9]\b:\b[0-9][0-9]\b:\b[0-9][0-9]',
            r'\bSRC=\b[0-9]+(?:\.[0-9]+){3}', r'\bDST=\b[0-9]+(?:\.[0-9]+){3}',
            r'\bSPT=\b[0-9]*', r'\bDPT=\b[0-9]*']

# joining(concatenating) full pattern with OR operator for better efficieny
pattern = "|".join(patterns)

# listtojson(temp)
# takes in a list containing one data entry
# example ['Dec 23', '17:04:40', '220.135.232.97', '192.168.133.189', '22934', '23']
# then properly maps each index to a python dictionary
# dictionary is then converted to json and then sent to backend to be appended into DB
def listtojson(temp):
    dict_items = {}
    index = 0

    for item in list_categories:
        dict_items[item] = temp[index]
        index += 1

    json_string = json.dumps(dict_items, indent=2)
    appbackend.jsontodb(json_string)

def formatdate(date):
    split_string = date.split(' ')
    newmonth = strptime(split_string[0],'%b').tm_mon
    format_date = ("2017" + str(newmonth).zfill(2) + split_string[1])
    return format_date

# formatlist(mylist)
# strips unwanted string from the parsed data list
# using a regular expression
# example 'SRC=192.12.32.2' -> '192.12.32.2'
# also converts port numbers (strings) -> integers
def formatlist(mylist):
    index = 0
    while index < len(mylist):
        mylist[index] = re.sub(r'[A-Z]*=', "", mylist[index])
        mylist[index].rstrip
        index += 1
    mylist[0] = formatdate(mylist[0])
    mylist[4] = int(mylist[4])
    mylist[5] = int(mylist[5])
    return mylist

def increment():
    global counter
    counter += 1

def totalcount():
    print ('Total lines parsed: ' + str(counter))

# opens the log file specified in field
# iterates line by line
# during each iteration each line is parsed with a regex to extract wanted data (thrown into temp list)
# list is then passed in as an argument to formatlist(temp) to trim off any unwated string & convert
# proper numbers to integers..
# this returns a list data type containing formatted entries
# formatlist(temp) is passed into listtojson(list data type), which communicates with the backend module..
# to append to database
def main(filename):
    appbackend.createIndex()
    with open(filename) as fn:
        for line in fn.readlines():
            temp = []
            temp.extend(re.findall(pattern, line))
            listtojson(formatlist(temp))
            increment()
        totalcount()

# run the program
main('log.txt')


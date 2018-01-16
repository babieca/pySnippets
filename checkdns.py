# -*- coding: utf-8 -*-

import dns.resolver
import requests
import re
import time
import MySQLdb
import sys


connection = MySQLdb.connect('', '', '', '')

cursor = connection.cursor()
cursor.execute("SELECT DISTINCT(lower(trim(word))) FROM table1 ORDER BY word;")
lstwords = cursor.fetchall()


connection.close()
    
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ["8.8.8.8", "8.8.4.4"]
resolver.nameservers = ["208.67.222.222", "208.67.220.220"]


filename='.../words.txt'

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

with open(filename, encoding='utf8') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 


#lstwords = []
for u in sorted(content, key=len):
    if isinstance(u, str):
        # [^\w] Match a single character not present in the list [a-zA-Z0-9_]
        u = re.sub(r'[^\w]', '', u)
        u = u.strip()
        u = u.lower()        
        lstwords.append(u)

lstwords = remove_duplicates(lstwords)

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
headers = {'User-Agent': ua}

for wrd in lstwords:
    time.sleep(0.1)
    try:
        public_ip = resolver.query(wrd + '.com')[0]
        #print(url + ' : ' + str(public_ip))
        
    except:
        #print(url, end='\n')
        churl = 'https://beta.companieshouse.gov.uk/company-name-availability?q=' + wrd
        page = requests.get(churl, headers=headers)
        
        if "No exact company name matches found for" in page.text:
            file = open('..../domains-available.txt', 'a')
            file.write(wrd+'\n')
            file.close()

sys.exit(0)
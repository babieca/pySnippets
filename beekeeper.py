#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import time
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


path_to_driver = './geckodriver-v0.19.1-linux64'   # Firefox driver
driver = webdriver.Firefox(executable_path = path_to_driver)
#driver.manage().window().setPosition(new Point(-2000, 0));

def wait_until_find_item(item, delay=3):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, item)))
        return True
    except TimeoutException:
        print "Loading took too much time!"
    return False

_username = ""
_password = ""

_url_login = "https://domain.com/login"
_url_logout = "https://domain.com/logout"
_url_msg = "https://domain.com/messages"

print("Loging in...")
driver.get(_url_login)

_submit_btn = '/html/body/div/div/form/button'
wait_until_find_item(_submit_btn)

driver.find_element_by_id('login_name').clear()
driver.find_element_by_id('password').clear()
driver.find_element_by_id('login_name').send_keys(_username)
driver.find_element_by_id('password').send_keys(_password)

driver.find_element_by_xpath(_submit_btn).click()


_home_icon = '/html/body/div[1]/div/nav/div/ul[1]/li[2]/a/i[1]'
wait_until_find_item(_home_icon)

counter = 5
pause = 3
lastHeight = driver.execute_script("return document.body.scrollHeight")

print("scrolling down a little...")
while counter >0:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight
    counter -= 1

posts =  driver.find_elements_by_class_name("post")
print("total posts found: " + str(len(posts)))

print("visiting messeges...")
driver.get(_url_msg)

_el1 = "/html/body/div[2]/div[1]/div/div[2]/div[1]/div["
_el2 = "]/div/div[2]/div"
_el3 = "/ul/li[1]/a"

_msg_div = 'listViewItem'
wait_until_find_item(_msg_div)
_msg =  driver.find_elements_by_class_name(_msg_div)
unread = 0
for i in range(1,len(_msg)):
    _drop_xpath = _el1 + str(i) + _el2
    _msg_xpath = _el1 + str(i) + _el2 + _el3
    el = driver.find_element_by_xpath(_drop_xpath)
    driver.execute_script("arguments[0].setAttribute('class','dropdown open')", el)
    lines = el.text
    for ln in lines.splitlines():
        if ln == 'Mark as Read':
            driver.find_element_by_xpath(_msg_xpath).click()
            unread += 1
            break
    driver.execute_script("arguments[0].setAttribute('class','dropdown')", el)

print("Total msg marked as read: " +str(unread) + "/" + str(len(_msg)))


time.sleep(pause)
print("Loging out...")
driver.get(_url_logout)

sys.exit(0)

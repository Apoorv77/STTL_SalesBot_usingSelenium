import os, random, sys, time
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver 
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print('Enter 1 to search for multiple keywords')
print('Enter 2 to search by a single hashtag')
s = -1
n = int(input())
if n==1:
    print('Enter keywords separated by space')
    keywords = input()
    s = 1
if n==2:
    print('Enter a hashtag')
    keywords = input()
    s = 2


browser = webdriver.Chrome(executable_path=r'./chromedriver.exe')
browser.get('https://www.linkedin.com/uas/login')
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)
elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
#link = 'https://www.linkedin.com/feed/hashtag/internships/'
#link = 'https://www.linkedin.com/search/results/content/?keywords=research%2C%20intern'
content = [i for i in keywords.strip().split(' ')]
if s == 1:
    link = 'https://www.linkedin.com/search/results/content/?keywords='
    for jj in range(len(content)):
        if jj != len(content)-1:
            link = link + content[jj] + '%20'
        if jj == len(content)-1:
            link = link + content[jj]
if s == 2:
    link = 'https://www.linkedin.com/feed/hashtag/'
    link = link + content[0] + '/'

browser.get(link)


SCROLL_PAUSE_TIME = 3
# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")
for i in range(10):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
connect_buttons = browser.find_elements_by_class_name('feed-shared-inline-show-more-text__see-more-less-toggle')
for connect_button in connect_buttons:
    #WebDriverWait(browser, 20).until(EC.element_to_be_clickable(connect_buttons)).click()
    connect_button.click()
    #print(connect_button)

timestamp = datetime.now()
src = browser.page_source
soup = BeautifulSoup(src, 'lxml')

master_data = soup.find_all('div', {'class': 'feed-shared-update-v2'})
info = soup.find_all('div', {'class':'feed-shared-actor__meta'})

no_pages=2
a=[]
base_link=browser.current_url
for j in range(1,no_pages+1):
    if(j>1):
        curr_link=base_link+"&page="+str(j)
        browser.get(curr_link)
    for i in range(1,11):
        path="//div[@id='search-marvel-srp-scroll-container']/div[1]/div[1]/ul[1]/li["+str(i)+"]/div[1]/div[1]"
        browser.find_element_by_xpath(path).click()
        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        master_data = soup.find_all('div', {'class': 'feed-shared-update-v2'})
        info = soup.find_all('div', {'class':'feed-shared-actor__meta'})
        try:
            post_obj={}
            Name = master_data[0].find_all('div', {'class': 'feed-shared-actor__meta relative'})[0].find('span', {'dir':'ltr'}).get_text().strip()
            post_obj['Name']=Name
            Post_Designation = master_data[0].find_all('span', {'class': 'feed-shared-actor__description'})[0].get_text().strip()
            Content = master_data[0].find_all('div', {'class': 'feed-shared-update-v2__description-wrapper'})[0].get_text().strip()
            post_obj['Content']=Content
            #print(Post)
            post_obj['Post_Designation']=Post_Designation
            #print(Content)
            Profile_URL=master_data[0].find('div', {'class': 'feed-shared-actor display-flex feed-shared-actor--with-control-menu'}).find('a', {'class':'app-aware-link feed-shared-actor__container-link relative display-flex flex-grow-1'})
            Profile_URL=str(Profile_URL)
            start_index=179
            end_index=Profile_URL.find('"',start_index)
            Profile_URL=Profile_URL[start_index:end_index]
            post_obj['Profile_URL']=Profile_URL
            a.append(post_obj)
        except:
            pass
print('$$$$$$$$$$$$$$$$$$$$$$$$$*******************************************************************$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

#Filter the posts -- to do

#Write to file
df = pd.DataFrame(a)
df.index = np.arange(1, len(df)+1)
df.to_excel ('Linked_Data_Leads.xlsx', sheet_name = 'sheet1')
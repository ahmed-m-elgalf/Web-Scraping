from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
import sys
from datetime import datetime

# get path of exe file
app_path = os.path.dirname(sys.executable)

now = datetime.now()
month_day_year = now.strftime("%m-%d-%Y, %H:%M:%S")



Options = Options()
Options.headless = True


s=Service('C:\\Users\\Ahmed\\Downloads\\chromedriver_win32\\chromedriver.exe')
browser = webdriver.Chrome(service=s , options=Options)
url='https://wuzzuf.net/a/IT-Software-Development-Jobs-in-Egypt?ref=browse-jobs&start=0'

browser.get(url)


last_page = 5

current_page = 1

li_links = []

while current_page < last_page :

    time.sleep(5) # stop 2 sec for page to load
    container = browser.find_element(By.XPATH,'//div[contains(@class,"css-9i2afk")]')
    books = container.find_elements(By.XPATH,'.//div[contains(@class,"css-1gatmva")]')


    for i in books:
        # extract href
        link = i.find_element(By.XPATH,'.//h2/a').get_property('href')
        print(link)
        li_links.append(link)
        # print(link)



    current_page = current_page+1
    try:
        next_page = browser.find_element(By.XPATH,'//div[contains(@class,"css-7o92qm")]//li[last()]//button')
        next_page.click()
    except:
        pass




alldetails=[]
for i in li_links:
    browser.get(i)

    # time.sleep(1)

    posted=browser.find_element(By.XPATH,'//span[contains(@class,"css-182mrdn")]').text

    title=browser.find_element(By.XPATH,'//h1[contains(@class,"css-f9uh36")]').text


    try:
        company=browser.find_element(By.XPATH,'//div[contains(@class,"css-9iujih")]/a').text
        print(company)

    except:
        applicant = 0
        pass



    try:
        applicant=browser.find_element(By.XPATH,'//strong[contains(@class,"css-u1gwks")]').text
        print(applicant)

    except:
        applicant = 0
        pass


    tools = []
    skills = browser.find_elements(By.XPATH,'//span[contains(@class,"css-6to1q")]')
    for x in skills:
        item = x.find_element(By.XPATH,'.//span[contains(@class,"css-158icaa")]').text

        tools.append(item)

    tempJ={
        'title':title,
        'company':company,
        'applicant':applicant,
        'link':i,
       'skills' : tools,
       'posted':posted,
       'date': str(now)

       }

    alldetails.append(tempJ)

df = pd.DataFrame(alldetails)


# file_name = f'wuzzuf-{month_day_year}.csv'

# final_path = os.path.join(app_path , file_name)

# df.to_csv(final_path ,  index= False)


# df = pd.DataFrame.from_dict(alldetails)


# df = pd.DataFrame(alldetails)


df.to_csv('wuzzuf-sql.csv' ,  index= False)


browser.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from datetime import datetime


now = datetime.now()
month_day_year = now.strftime("%m-%d-%Y, %H:%M:%S")
Options = Options()
Options.headless = True

# Get current working directory
current_directory = os.getcwd()
chrome_driver_path= os.path.join(current_directory, 'chromedriver.exe')
s=Service(chrome_driver_path)


browser = webdriver.Chrome(service=s , options=Options)
url='https://wuzzuf.net/a/IT-Software-Development-Jobs-in-Egypt?ref=browse-jobs&start=0'

browser.get(url)


def extract_job_details(job_element):
    try:
        company = job_element.find_element(By.XPATH, '//div[contains(@class,"css-9iujih")]/a').text
    except:
        company = ""
    try:
        applicant = job_element.find_element(By.XPATH, '//strong[contains(@class,"css-u1gwks")]').text
    except:
        applicant = 0
    skills_elements = job_element.find_elements(By.XPATH, '//span[contains(@class,"css-6to1q")]')
    tools = [x.find_element(By.XPATH, './/span[contains(@class,"css-158icaa")]').text for x in skills_elements]
    return company, applicant, tools



last_page = 5
current_page = 1
li_links = []


while current_page < last_page :
    time.sleep(5) 
    container = browser.find_element(By.XPATH,'//div[contains(@class,"css-9i2afk")]')
    jobs = container.find_elements(By.XPATH,'.//div[contains(@class,"css-1gatmva")]')


    for i in jobs:
        link = i.find_element(By.XPATH,'.//h2/a').get_property('href')
        print(link)
        li_links.append(link)

    current_page += 1
    try:
        next_page = browser.find_element(By.XPATH,'//div[contains(@class,"css-7o92qm")]//li[last()]//button')
        next_page.click()
    except:
        pass


alldetails=[]
for i in li_links:
    browser.get(i)
    posted=browser.find_element(By.XPATH,'//span[contains(@class,"css-182mrdn")]').text
    title=browser.find_element(By.XPATH,'//h1[contains(@class,"css-f9uh36")]').text
    company, applicant, skills = extract_job_details(browser)
    tempJ={
        'title':title,
        'company':company,
        'applicant':applicant,
        'link':i,
       'skills' : skills,
       'posted':posted,
       'date': str(now)

       }
    alldetails.append(tempJ)

df = pd.DataFrame(alldetails)
df.to_csv('wuzzuf.csv' ,  index= False)


browser.quit()
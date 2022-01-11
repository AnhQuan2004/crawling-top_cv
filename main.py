#Import the packages
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager

from bs4 import BeautifulSoup

import time
import json
import re

from datetime import datetime
from datetime import timedelta


#Define 
all_link = []
content = []
all_link_del_duplicates = []
notice = 'Information is missed'


#Chrome Options
option = webdriver.FirefoxOptions()
option.add_argument ('--ignore-certificate-errors')
option.add_argument ("--igcognito")
option.add_argument ("--window-size=1920x1080")
#option.add_argument ('--headless')
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-shm-usage")


#Set path for webdriver
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=option)

#Open log-in url
driver.get("https://secure.vietnamworks.com/login/vi?client_id=3") 
driver.maximize_window()


#Time-wait
time.sleep(10)


#Fill the log-in information
driver.find_element_by_id("email").send_keys("")
driver.find_element_by_id('login__password').send_keys("")
driver.find_element_by_id("button-login").click()

#Crawl all the links of job
url = 'https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam'
driver.get(url)
time.sleep(3)

page_num = 1
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

while True:
    #crawl all the link in each page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,"html.parser")
    block_job_list = soup.find_all("div",{"class":"block-job-list"})
    for i in block_job_list:
        link_catalogue = i.find_all("div",{"class":"col-12 col-lg-8 col-xl-8 p-0 wrap-new"})
        for j in link_catalogue:
            link = j.find("a")
            all_link.append("https://www.vietnamworks.com" + link.get("href"))

    # moves to next page
    try:
        print(f'On page {str(page_num)}')
        print()
        page_num+=1
        driver.find_element_by_link_text(str(page_num)).click()
        time.sleep(3)

    # checks only at the end of the page
    except NoSuchElementException:
        print('End of pages')
        break

#Remove all duplicates links
[all_link_del_duplicates.append(x) for x in all_link if x not in all_link_del_duplicates]

print("\n".join(all_link_del_duplicates))
print(len(all_link_del_duplicates))

datas = {}
datas['jobs'] = []

#Enter to every links to crawl the data
for url in all_link_del_duplicates:
    page = driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    name_job = soup.find("h1",{"class":"job-title"}).text.replace("\n","").strip()

    name_company = soup.find("div",{"class","company-name"}).text.replace("\n","").strip()

    name_location = soup.find("span",{"class":"company-location"}).text.replace("\n","").strip()

    salary = soup.find("span",{"class":"salary"}).text.replace("\n","").strip()

    for i in soup.find_all("div",{"class":"benefits"}):
        benefits = " ".join(i.text.split())

    job_description = soup.find("div",{"class":"job-description"})
    for i in job_description.find_all("div",{"class":"description"}):
        description = i.text.replace("\n","").replace("\r","").replace("\t","").strip()

    for i in soup.find_all("div",{"class":"requirements"}):
        requirements = i.text.replace("\n","").replace("\r","").replace("\t","").strip()

    information = soup.find_all("div",{"class":"row summary-item"})
    for i in information:
        content.append(i.find("span",{"class":"content"}).text.replace('\xa0','').replace('\n', '').replace('  ',"").strip())

    try:
        upload_date = content[0]
    except IndexError:
        upload_date = notice

    expiration_str = soup.find("span",{"class":"expiry"}).text.replace("\n","").strip()
    number_expiration_date = re.findall(r'\d+', expiration_str)[0]

    expiration_date = (datetime.strptime(upload_date, '%d/%m/%Y').date() + timedelta(days=int(number_expiration_date))).strftime('%d/%m/%y')

    try:
        position = content[1]
    except IndexError:
        position = notice

    try:
        career = content[2]
    except IndexError:
        career = notice

    try:
        skill = content[3]
    except IndexError:
        skill = notice

    try:
        language_of_cv = content[4]
    except IndexError:
        language_of_cv = notice

    try:
        detail_address = content[5]
    except IndexError:
        detail_address = notice

    try:
        number_employees = content[6]
    except IndexError:
        number_employees = notice


    data = {
        "name": name_job,
        "salary": salary,
        "upload_date": upload_date,
        "expiration_date": expiration_date,
        "locations": name_location,
        "skill": skill,
        "career": career,
        "company": name_company,
        "job_position": position,
        "number_employees": number_employees,
        "detail_address": detail_address,
        "language_cv": language_of_cv,
        "benefits": benefits,
        "description": description,
        "requirements": requirements,
        "link_job" : url,
    }
    
    datas['jobs'].append(data)

driver.quit()

file = open("vietnamworks.json", "w")
json.dump(datas, file)
file.close()

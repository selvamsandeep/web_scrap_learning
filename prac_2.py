# http://www.ite-exhibitions.com/event-calendar.aspx


import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import random


seconds = 5 + (random.random() * 5)
driver = webdriver.Chrome(executable_path='/home/selva/crome_driver/chromedriver')
driver.implicitly_wait(30)


url = "http://www.ite-exhibitions.com/event-calendar.aspx"
driver.get(url)
sleep(seconds)
sleep(seconds)

while True:
    try:
        element = driver. \
        find_element_by_id("p_lt_ctl04_pageplaceholder_p_lt_ctl02_EventUC_userControlElem_btnShowMore")
    except:
        break
   
    driver.execute_script("arguments[0].click();", element)
    sleep(seconds)
    sleep(seconds)
    
    
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

events = soup.find_all(class_="event-item")
print('Total events: ', len(events))

driver.quit()

#! python3
# 'http://www.ite-exhibitions.com'

events_links = []
base_url = 'http://www.ite-exhibitions.com'
for event in events:    
    events_links.append(base_url + event.find('a').get('href'))
    
event_name = []
org_url = []
event_date = []
event_location = []
event_contact_email = []
org_name = []

def get_events_details():    
    for url_ in events_links:
        #print(url_)
        soup1 = BeautifulSoup(urlopen(url_).read(), 'lxml')
        event_details = soup1.find(class_="eventdetails").get_text().lstrip().split('\n')
        event_name.append(event_details[0])
        org_url.append(soup1.find(class_="eventdetails").find('a').get('href'))
        event_date.append(event_details[1].lstrip())
        event_location.append(event_details[3].lstrip())
        event_contact_email.append(soup1.find(id="side_event_details").find('a').get('href').split(':')[1])
        org_name.append(soup1.find(class_="selected_event_detail_item").text.split(':')[1])
        sleep(seconds)
    
def create_dataframe(): 
    df = pd.DataFrame()
    df['record'] = np.arange(1, len(event_name)+1)
    df['event_name'] = event_name
    df['event_url'] = events_links
    df['event_date'] = event_date
    df['event_start'] = ""
    df['event_end'] = ""
    df['event_location'] = event_location
    df['event_venue'] = ""
    df['event_city'] = ""
    df['event_country'] = ""
    df['event_contact_email'] = event_contact_email
    df['event_punchline'] = ""
    df['event_edition'] = ""
    df['org_name']  = org_name
    df['org_website'] = org_url
    df['org_email'] = ""
    df['fk_category_1'] = ""
    df['fk_category_2'] = ""
    df['fk_venue_id'] = ""
    df['fk_city_id'] = ""
    df['fk_country_id'] = ""
    df['fk_event_id'] = ""
    df['fk_event_type'] =""
    return df

if __name__=='__main__':
    
    print('getting  events details')
    get_events_details()    
    
    df = create_dataframe()
    date_run = datetime.today().strftime('%d-%m-%y')
    df.to_csv('rawdata_007_'+ date_run +'.csv', index=False)
            

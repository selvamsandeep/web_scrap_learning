#https://www.ubm.com/find-an-even
# modified 28/12/18

import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://www.ubm.com/find-an-event?page=%d"

defaultPage = 0
def getWebsiteContent(page=defaultPage):
    return urlopen(url % (page)).read()

content = getWebsiteContent(page=0)
soup = BeautifulSoup(content, 'lxml')

total_events = int(soup.find(class_="resultCount").text.split(' ')[0])
events_per_page = 30
num_page = (total_events // events_per_page) + 1
#print(total_events, num_page)

def get_event_date(dates):
    start = dates[0].text.replace(',', '').split(' ')[1] 
    end = dates[1].text.replace(',', '').split(' ')[1] 
    month = dates[0].text.replace(',', '').split(' ')[0]
    year = dates[0].text.replace(',', '').split(' ')[2]
    return start + '-' + end + ' ' + month + ' ' + year
#get_event_date(row.find(class_="date").find_all('time'))    

event_name = []
event_url = []
event_date = []
event_location = []
event_punchline = []

def get_envet_details():
    for page in range(num_page):
        content = getWebsiteContent(page)
        soup = BeautifulSoup(content, 'lxml')
        rows = soup.find('tbody').find_all('tr')
        for row in rows: 
            #print(row.find(class_="title").text)
            event_name.append(row.find(class_="title").text)
            dates = row.find(class_="date").find_all('time')
            event_date.append(get_event_date(dates))
            #event_start.append(time[0].text)
            #event_end.append(time[1].text)

            event_punchline.append(row.find(class_="body").text)
            #print(row.find('a').get('href'))
            event_location.append(row.find(class_="region").text)
            #event_category.append(row.find(class_ = "eventcategory").text)
            #event_subcategory.append(row.find(class_ = "eventsubcategory").text)
            if row.find('a'):
                event_url.append(row.find('a').get('href'))
            else:
                event_url.append("")
                
def create_dataframe():  
    df = pd.DataFrame()
    df['record'] = np.arange(1, len(event_name)+1)
    df['event_name'] = event_name
    df['event_url'] = event_url
    df['event_date'] = event_date
    df['event_start'] = ""
    df['event_end'] = ""
    df['event_location'] = event_location
    df['event_venue'] = ""
    df['event_city'] = ""
    df['event_country'] = ""
    df['event_contact_email'] = ""
    df['event_punchline'] = event_punchline 
    df['event_edition'] = ""
    df['org_name']  = ""
    df['org_website'] = ""
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
    
    print('getting ubm events details')
    get_envet_details()    
    
    df = create_dataframe()
    date_run = datetime.today().strftime('%d-%m-%y')
    df.to_csv('rawdata_003_'+ date_run +'.csv', index=False)



#https://www.messefrankfurt.com/frankfurt/en/event-search.html
#modified 28/12
import numpy as np
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from datetime import datetime
import calendar
import re

url = "https://eventsearch.messefrankfurt.com/service/esb/1.0/event/search/en?q=&orderBy=date&pageNumber=%d&pageSize=50"

defaultPage = 1
def getWebsiteContent(page=defaultPage):
    return urlopen(url % (page)).read()

content = getWebsiteContent(page=1)
soup = BeautifulSoup(content, 'lxml')

total_events = json.loads(soup.find('p').text)['result']['metaData']['hitsTotal']
events_per_page = json.loads(soup.find('p').text)['result']['metaData']['hitsPerPage']
num_page = (total_events // events_per_page) + 1
print('total_events: ',total_events, 'events_per_page: ', events_per_page, 'pages: ',num_page)

def get_event_date(start, end):
    st = start.split('-')[2]
    ed = end.split('-')[2]
    mn = int(end.split('-')[1])
    yr = end.split('-')[0]
    return st + '-' + ed + ' ' + calendar.month_abbr[mn] + ' ' + yr

event_name = []
event_url = []
event_date =[]
event_location =[]
event_contact_email =[]
event_venue = []
event_punchline = []
org_name = []


def get_events_details():   

    for page in range(1, num_page + 1):
        content = getWebsiteContent(page=page)
        soup = BeautifulSoup(content, 'lxml')
        events = json.loads(soup.find('p').text)['result']['hits']
        for event in events:
            event_name.append(event['eventname'])
            event_url.append(event['interneturl'])        
            event_date.append(get_event_date(event['startdate'], event['enddate']))        
            event_location.append(event['cityname'])
            event_venue.append(event['venuename'])
            event_punchline.append(event['subtitle'])
            org_name.append(event['organizer'])
            event_contact_email.append(event['contactemail'])    
            
def create_dataframe():  
    df = pd.DataFrame()
    df['record'] = np.arange(1, len(event_name)+1)
    df['event_name'] = event_name
    df['event_url'] = event_url
    df['event_date'] = event_date
    df['event_start'] = ""
    df['event_end'] = ""
    df['event_location'] = event_location
    df['event_venue'] = event_venue 
    df['event_city'] = ""
    df['event_country'] = ""
    df['event_contact_email'] = event_contact_email
    df['event_punchline'] = event_punchline 
    df['event_edition'] = ""
    df['org_name']  = org_name
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
    
    print('getting events details')
    get_events_details()    
    
    df = create_dataframe()
    date_run = datetime.today().strftime('%d-%m-%y')
    df.to_csv('rawdata_005_'+ date_run +'.csv', index=False)
            
            

#!/usr/bin/env python
# coding: utf-8


#import package
from bs4 import BeautifulSoup
import requests
import pandas as pd

def search_weather(city):
    # access different weathr codeby user input
    city_code = ''
    if city.lower() == 'new york':
        city_code = 'NY0996'
    elif city.lower() == 'los angeles':
        city_code = 'NY0996'
    elif city.lower() == 'seattle':
        city_code = 'WA0395'
    elif city.lower() == 'boston':
        city_code = 'MA0046'
    else :
        city_code = 'PA1290'

    # generate the url for scrapping
    page = requests.get('https://weather.com/weather/tenday/l/US'+ city_code + ':1:US')
    
    # get html
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # parsing the data in html
    table_rows = soup.find(id="twc-scrollabe").tbody.find_all("tr")
    
    # parsing the selected content
    all_weather = []
    col_day = soup.find(class_="twc-sticky-col").get_text()
    col_desc = soup.find(class_="description").get_text()
    col_temp = soup.find(class_="temp").get_text()
    col_prec = soup.find(class_="precip").get_text()
    col_wind = soup.find(class_="wind").get_text()
    col_hum = soup.find(class_="humidity").get_text()
    all_weather.append([col_day, col_desc, col_temp, col_prec, col_wind, col_hum])
    
    # create weather list by date and append it into all_weather list
    for tr in table_rows:
        one_day = []
        one_day.append(tr.find(class_ = "day-detail").text)
        one_day.extend((tr.find(class_ = "description").text, 
                       str(tr.find(class_ = "temp").text), 
                       tr.find(class_ = "precip").text, 
                       tr.find(class_ = "wind").text, 
                       tr.find(class_ = "humidity").text))
        all_weather.append(one_day)
    # create a dataframe by list
    weather_dataframe = pd.DataFrame(((dd for dd in d[1:]) for d in all_weather[1:]), columns=all_weather[0][1:], index=list(d[0] for d in all_weather[1:]))
    return weather_dataframe


# In[33]:
if __name__ == '__main__':
    search_weather("seattle")






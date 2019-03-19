#!/usr/bin/env python
# coding: utf-8

#imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

# In[37]:


# store URL and state name
urlbook = {"pittsburgh": ['https://www.tripadvisor.com/Attractions-g53449-Activities-Pittsburgh_Pennsylvania.html', 'PA'],
           "boston": ['https://www.tripadvisor.com/Attractions-g60745-Activities-Boston_Massachusetts.html', 'MA'],
           "new york": ['https://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html','NY'],
           "seattle": ['https://www.tripadvisor.com/Attractions-g60878-Activities-Seattle_Washington.html', 'WA'],
           "los angeles": ['https://www.tripadvisor.com/Attractions-g32655-Activities-Los_Angeles_California.html', 'CA']}


# Pittsburgh's tripadvisor webpage has different html structure from other cities
def PittsScrape(cityname, tatrip):
    sites = tatrip.find_all(attrs = {"class": "poi"})
    attractions = {}
    for i in sites:
        line = i.get_text(';').split(";")
        name = line[1]
        line[2] = line[2].replace(",","")
        review = int(line[2][:line[2].index("Review")])
        rate = int(i.span['class'][1][7:])/10
        category = line[3]
        link = "https://www.tripadvisor.com"+i.find("a").get("href")
        imgID = i.img["id"]
        address = name + "," + cityname + ", "+ urlbook[cityname][1]
        l = [name, address, rate, review, "", category, link, imgID, "", ""]
        attractions[name] = l
    images = tatrip.find(string = re.compile("var lazyImgs")).split("data")
    imglinks = {}
    for i in images:
        try:
            iid = i[i.index("lazyload"):i.index('priority')-3]
            link = i[i.index("http"):i.index(".jpg")+4]
            imglinks[iid] = link
        except:
            pass
    for i in attractions:
        try:
            attractions[i[0]][7] = imglinks[i[1][7]]
        except:
            pass
    return attractions
    # with open('tatrip_data.txt', 'w') as handle:
    #    handle.writelines('Name; Address; Rating; Popularity; Price; Category; URL; ImageURL; Phone; Description\n')
    #    for i in attractions.values():
    #        handle.writelines(i[0]+';'+i[1]+';'+i[2]+';'+str(i[3])+';'+str(i[4])+';'+i[5]+';'+i[6]+';'+i[7]+'\n')


# In[43]:


def OtherScrape(cityname, tatrip):
    sites = tatrip.find_all(attrs = {"class": "attractions-attraction-overview-main-TopPOIs__item--e3w3i"})
    attractions = {}
    for i in sites:
        line = i.get_text(';').split(";")
        name = line[3]
        line[4] = line[4].replace(",","")
        review = int(line[4][:line[4].index("review")])
        num = str(i).index("ui_bubble_rating bubble_")+len("ui_bubble_rating bubble_")
        rate = int(str(i)[num:num+2])/10
        category = line[1]
        link = "https://www.tripadvisor.com"+i.find("a").get("href")
        img = i.find("img").get("data-url")
        img = img[:img.index(".jpg")+4]
        address = name + "," + cityname + ", "+ urlbook[cityname][1]
        l = [name, address, rate, review, "", category, link, img, "", ""]
        attractions[name] = l
    return attractions
    # with open('tatrip_data.txt', 'w') as handle:
    #     handle.writelines('Name; Address; Rating; Popularity; Price; Category; URL; ImageURL; Phone; Description\n')
    #     for i in attractions.values():
    #         handle.writelines(i[0]+';'+i[1]+';'+i[2]+';'+str(i[3])+';'+str(i[4])+';'+i[5]+';'+i[6]+';'+i[7]+'\n')


# In[40]:

def init(city):
    city = city.lower()
    # extract HTML for the selected city
    searchURL = urlbook[city][0]
    html = urlopen(searchURL)
    tatrip = BeautifulSoup(html.read(), features="html.parser")
    if city.lower() == "pittsburgh":
        data = PittsScrape(city.lower(), tatrip)
    else:
        data = OtherScrape(city.lower(), tatrip)
    columns = ["Name", "address", "rating", "popularity", "price", "category", "url", "imageurl", "phone", "description"]
    attraction_df = pd.DataFrame.from_dict(data, orient="index", columns=columns)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(attraction_df)
    return attraction_df


# In[33]:
if __name__ == '__main__':
    init("seattle")




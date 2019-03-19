
# coding: utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


# The hotel_main method extracts the information from the hotels.com website. The method takes in the
# string of the city name, check in date, and check out date, and uses the selenium with chrome driver
# and beautifulsoup to extract information from the website.
def hotel_main(city, checkInDate, checkOutDate):
    url = "https://www.hotels.com/"
    urlsAndCities = set()
    completeUrl = url
    completeUrl += "search.do?q-destination=" + city + "&q-check-in=" + checkInDate + "&q-check-out=" + checkOutDate

    # Open the chrome driver, scroll down using selenium and get the whole html page; find all the hotel tags
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get(completeUrl)
    body = driver.find_element_by_css_selector('body')
    for num in range(400):
        body.send_keys(Keys.PAGE_DOWN)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, features="html.parser")
    hotels = soup.find_all(class_="hotel-wrap")
    result = {}

    # for each hotel html part, extract information from the block
    for hotel in hotels:
        name = hotel.find(class_="p-name").text.strip()
        street = hotel.find(class_="contact").text.strip()[:-14]
        phone = hotel.find(class_="contact").text.strip()[-12:]
        try:
            guest_reviews = hotel.find(class_="guest-reviews-badge").text.strip()[-3:]
            guest_reviews = str(float(guest_reviews) / 10 * 5)

        except:
            guest_reviews = None
        try:
            popularity = hotel.find(class_="small-view").text.strip()[:-8].replace(',', '')
        except:
            popularity = None
        try:
            price = hotel.find(class_="price").text.strip()
            digits = [int(s) for s in price.split("$") if s.isdigit()]
            price = digits[-1]
        except:
            price = None

        result[name] = [name, street, guest_reviews, popularity, price, "", "", "", phone, ""]

    # Construct the dataframe from the combined dictionary in the indexed order
    columns = ["Name", "address", "rating", "popularity", "price", "category", "url", "imageurl", "phone",
               "description"]
    df = pd.DataFrame.from_dict(data=result, orient="index", columns=columns)
    return df


if __name__ == '__main__':
    hotel_main("Pittsburgh", "2019-03-01", "2019-03-02")



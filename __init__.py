
import restaurants_scraping as restaurant
import hotel_scraping as hotel
import FP_weather_scrapping as weather
import attraction_scraping as attraction
import sort_filter as sf
import pandas as pd
import datetime as dt
import packaging as pg
import numpy as np
import calculate_distance as cd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np


CATEGORY_HOTEL = "hotel"
CATEGORY_RESTAURANT = "restaurant"
CATEGORY_ATTRACTION = "attraction"


# this is the main class that initiate all scrapping and data processing

# this method will call all data scrapping method to scrap required data
def scrap_data(location, start_date, end_date, preference=None):

    print("Scraping restaurants...")
    restaurant_data = restaurant.scrap(location)

    print("Scarping hotels...")
    hotel_data = hotel.hotel_main(location, start_date, end_date)

    print("Scraping attractions...")
    attraction_data = attraction.init(location)

    print("Scrapping weather...")
    weather_data = weather.search_weather(location)

    return restaurant_data, hotel_data, attraction_data, weather_data


# this method will sort and filter based on user's preference
def data_filter(restaurant_data, hotel_data, attraction_data, preference, num_days):
    hotel_filtered = sf.sort_n_filter(hotel_data, preference, CATEGORY_HOTEL, num_days)
    restaurant_filtered = sf.sort_n_filter(restaurant_data, preference, CATEGORY_RESTAURANT, num_days)
    attraction_filtered = sf.sort_n_filter(attraction_data, preference, CATEGORY_ATTRACTION, num_days)
    return hotel_filtered, restaurant_filtered, attraction_filtered


# this method is a helper method that replace name with actual address in dataframe
def route_to_address(routes, hotel_filtered, attraction_filtered, restaurant_filtered):
    route_address = {}
    for index, row in routes.iterrows():
        daynum = 1
        route_address[index] = {}
        for day in row:
            route_address[index]['day{}'.format(daynum)]=[]
            for i in range(len(day)):
                if i == 0 or i == 5:
                    route_address[index]['day{}'.format(daynum)].append(hotel_filtered.loc[day[i], "address"])
                if i == 1 or i == 3:
                    route_address[index]['day{}'.format(daynum)].append(attraction_filtered.loc[day[i], "address"])
                if i == 2 or i == 4:
                    route_address[index]['day{}'.format(daynum)].append(restaurant_filtered.loc[day[i], "address"])
            daynum += 1;
    route_address = pd.DataFrame.from_dict(route_address)
    return route_address


# this method gathers all data and compose a final dataframe that will pass to front end
def to_route_output(routes, hotel_filtered, attraction_filtered, restaurant_filtered):
    for index, row in routes.iterrows():
        for day in row:
            for i in range(len(day)):
                if i == 0 or i == 5:
                    day[i] = hotel_filtered.loc[day[i]]
                if i == 1 or i == 3:
                    day[i] = attraction_filtered.loc[day[i]]
                if i == 2 or i == 4:
                    day[i] = restaurant_filtered.loc[day[i]]
    return routes


# this method will compose a data plot that help use to find better route
def export_plot(route_distance, routes):
    distance_list = []
    time_list = []
    for index in route_distance.index:
        distance = 0
        time = 0
        for day in route_distance.loc[index]:
            for pair in day:
                distance += float(pair[0].split(" ")[0].strip())
                time += float(pair[1].split(" ")[0].strip())
        distance_list.append(distance)
        time_list.append(time)

    y = distance_list
    N = len(y)
    x = ['Route 1', 'Route 2', 'Route3']

    plt.figure(1)
    plt.bar(x, y, width=0.5, color="pink", label='Distance in total')
    plt.title("Distance Comparison")
    plt.savefig("./img/traffic.png")

    rating_list = []
    pop_list = []
    for route in range(3):
        rating = 0
        pop = 0
        for day in range(len(routes.iloc[0])):
            for day_len in range(len(routes.iloc[route][day])):
                rating += float(routes.iloc[route][day][day_len]['rating'])
                pop += float(routes.iloc[route][day][day_len]['popularity'])
        rating_list.append(rating / (day_len + 1))
        pop_list.append(pop / (day_len + 1))

    day_len = len(routes.iloc[0])
    pop_list_plot = np.array(pop_list) / day_len
    rating_list_plot = np.array(rating_list) / day_len

    x = ['Route 1', 'Route 2', 'Route3']
    plt.figure(2)
    plt.bar(x, pop_list_plot, width=0.5, color="skyblue", label='Average Popularity')
    plt.title("Popularity Comparison")
    plt.savefig("./img/popularity.png")

    x = ['Route 1', 'Route 2', 'Route3']
    plt.figure(3)
    plt.bar(x, rating_list_plot, width=0.5, color="tomato", label='Average Rating')
    plt.title("Rating Comparison")
    plt.savefig("./img/rating.png")


def init(location, start_date, end_date, preference):
    print("Application Start...")
    # get number of days
    start_dt = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_dt = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    num_days = (end_dt - start_dt).days
    print("Number of days: {}".format(num_days))

    # scrap data
    restaurant_data, hotel_data, attraction_data, weather_data = scrap_data(location, start_date, end_date, preference)

    # filter data
    # print("###################################################")
    print("Sorting data with preference 【{}】 and filtering...".format(preference))
    hotel_filtered, restaurant_filtered, attraction_filtered = data_filter(restaurant_data,
                                                                           hotel_data,
                                                                           attraction_data,
                                                                           preference,
                                                                           num_days)
    # print("\n\n#########filtered#########")
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'expand_frame_repr', False):
    #     print(hotel_filtered)
    #     print(restaurant_filtered)
    #     print(attraction_filtered)

    # calculate distances between POIs and package them to bundles
    print("\n\nCalculating Distance...")
    attraction_restaurant_package = cd.package_att_rest(attraction_filtered, restaurant_filtered)
    attraction_restaurant_package_filtered = [item for item in attraction_restaurant_package
                                              if int(item[2]) <= 20000]

    # package items to actual routes
    print("Calculating distances between each POI ...")
    routes = pg.package(hotel_filtered, attraction_restaurant_package_filtered, num_days)

    # transform name df to address df
    route_address = route_to_address(routes, hotel_filtered, attraction_filtered, restaurant_filtered)
    route_distance = cd.calculate_each_route(route_address)
    print("\n\n#########route_distance#########")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'expand_frame_repr', False, 'display.max_colwidth', -1):
        print(route_distance)

    # replace name in route with actual POI contents
    print("\n\n#########Final_route_outputs#########")
    routes = to_route_output(routes, hotel_filtered, attraction_filtered, restaurant_filtered)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', -1):
        print(routes)

    print("\n\n#########Weather_outputs#########")
    weather_output = weather_data[["Description", "High / Low"]]
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', -1):
        print(weather_output)

    export_plot(route_distance, routes)

    return routes, route_distance, weather_output


if __name__ == '__main__':
    init("new york", "2019-02-25", "2019-02-26", "popularity")


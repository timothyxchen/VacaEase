#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import urllib
import json
import datetime
import re


def request_data_from_url(url):
    success = False
    while success is False:
        try:
            response = urllib.request.urlopen(url)
            # print("text: ", response)
            if response.getcode() == 200:
                success = True
                # print("reponse is 200")
        except:
            print("Error for URL %s: %s" % (url, datetime.datetime.now()))
            print("Retrying...")
    return response.read()


# In[105]:

def calculate_distance(origin, destination, len_ori, len_des):
    # origin = location_to_la_lon(origin_text)
    # destination = location_to_la_lon(destination_text)

    api_key = 'AIzaSyCnDe435hF8VQXwUD4t8m8y_0CxWBlKEYU'
    site = 'https://maps.googleapis.com/maps/api/'
    service = 'distancematrix/json?'
    locations = 'origins=%s&destinations=%s&departure_time=now&' % (origin, destination)
    key = 'key=%s' % (api_key)
    request_url = site + service + locations + key
    # print(request_url)
    response = request_data_from_url(request_url)
    data = json.loads(response, encoding='bytes')
    distance = []
    for i in range(len_ori):
        row = []
        for j in range(len_des):
            if data['rows'][i]['elements'][j]['status'] != 'OK':
                row.append('-1')
            else:
                row.append(data['rows'][i]['elements'][j]['distance']['value'])

        distance.append(row)

    return np.array(distance)


# input  dataframe
# output numpy array, each row is a package
# unit of distance:  meters
def package_att_rest(att_df, rest_df):
    att_name_list = list(att_df['Name'])
    att_add_list = list(att_df['address'])
    rest_name_list = list(rest_df['Name'])
    rest_add_list = list(rest_df['address'])
    len_res = len(rest_name_list)
    len_att = len(att_name_list)
    rest_input = '|'.join(list(rest_add_list))
    att_input = '|'.join(list(att_add_list))
    package = []

    for i in range(len_res):
        print("Calculating distance for {} <---> {}".format(rest_add_list[i], att_input))
        distance = calculate_distance(urllib.parse.quote_plus(rest_add_list[i]), urllib.parse.quote_plus(att_input), 1, len_att)
        for j in range(len_att):
            if (float(distance[0][j]) > 0):
                temp = []
                temp.append(rest_name_list[i])
                temp.append(att_name_list[j])
                temp.append(distance[0][j])
                package.append(temp)

    np_package = np.array(package)
    dis_list = [float(i) for i in np_package[:, 2]]
    result = np_package[np.array(dis_list).argsort()]
    # package = np.array(package)
    # result = package[package[:,2].argsort()]
    return result


def calculate_distance_second(package_list):
    # origin = location_to_la_lon(origin_text)
    # destination = location_to_la_lon(destination_text)
    len_package = len(package_list)
    origin_list = package_list[:-1]
    destination_list = package_list[1:]

    origin_input = '|'.join(origin_list)
    des_input = '|'.join(destination_list)

    origin = re.sub(r"\s", "+", origin_input)
    destination = re.sub(r"\s", "+", des_input)
    api_key = 'AIzaSyCnDe435hF8VQXwUD4t8m8y_0CxWBlKEYU'
    site = 'https://maps.googleapis.com/maps/api/'
    service = 'distancematrix/json?'
    locations = 'origins=%s&destinations=%s&departure_time=now&' % (urllib.parse.quote_plus(origin), urllib.parse.quote_plus(destination))
    key = 'key=%s' % (api_key)

    request_url = site + service + locations + key
    # print(request_url)
    reponse = request_data_from_url(request_url)
    data = json.loads(reponse, encoding='bytes')
    distance = []
    distance.append(['0', '0'])
    for i in range(len_package - 1):
        row = []
        if data['rows'][i]['elements'][0]['status'] != 'OK':
            row.append('NULL')
            row.append('NULL')
        else:
            row.append(data['rows'][i]['elements'][i]['distance']['text'])
            row.append(data['rows'][i]['elements'][i]['duration']['text'])
            distance.append(row)

    return distance


def calculate_each_route(route_df):
    result = {}
    for i in route_df.index:
        route_i_dic = {}
        for j in route_df:
            route_i_D_j = route_df.loc[i, j]  # is a list of address
            result_for_route_i_D_j = calculate_distance_second(route_i_D_j)
            route_i_dic[j] = result_for_route_i_D_j
        result[i] = route_i_dic
    # print(result)
    # result_pd = pd.DataFrame(result, index = route_df.index)
    result_df = pd.DataFrame.from_dict(data=result)
    return result_df


if __name__ == '__main__':
    att_df = pd.read_csv('att.csv')
    rest_df = pd.read_csv('rest.csv')
    print(type(att_df))
    test_package = package_att_rest(att_df, rest_df)
    test_package


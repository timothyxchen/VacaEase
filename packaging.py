#!/usr/bin/env python
# coding: utf-8

import random
import pandas as pd
from random import randint


# The package method will take the hotel dataframe, attraction and restaurant bundles, and number of days the
# user input. This method will return a dataframe which contains the the differnt daily schedule of different
# days in different routes.
def package(hotel,bundle_set,numDays):
    # bundle_set=bundle_set.tolist()
    # hotel=hotel.iloc[:,0].iloc[(random.randint(1,len(hotel.iloc[:,0])-1))]
    package_result={}
    num_item = numDays * 10
    for i in range(3):
        hotel_name = hotel.iloc[:, 0].iloc[(random.randint(1, len(hotel.iloc[:, 0])) - 1)]
        bundleset_copy=bundle_set.copy()
        route={}
        for j in range(numDays):
            day_schedule=[]
            day_schedule.append(hotel_name)
            random.shuffle(bundleset_copy[:num_item])

            # Get the result for bundle1
            bundle1=bundleset_copy[:num_item].pop(randint(0,num_item-1))
            bundleset_copy=[bundle for bundle in bundleset_copy if bundle[0] != bundle1[0] and bundle[1] != bundle1[1]]
            day_schedule.append(bundle1[1])
            day_schedule.append(bundle1[0])

            random.shuffle(bundleset_copy[:num_item])
            #bundle2
            bundle2=bundleset_copy[:num_item].pop(randint(0,num_item-1))
            bundleset_copy=[bundle for bundle in bundleset_copy if bundle[0] != bundle2[0] and bundle[1] != bundle2[1]]
            day_schedule.append(bundle2[1])
            day_schedule.append(bundle2[0])

            day_schedule.append(hotel_name)
            route["day"+str(j+1)]=day_schedule
        package_result["route"+str(i+1)]=route
    df = pd.DataFrame.from_dict(data=package_result, orient="index")
    return df
        


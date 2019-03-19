#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import random


# this class sort and filter scrapped data based on user's preference input

def sort_n_filter(data, preference, category, days):
    # delete missing value
    data = data.drop(['description'], axis = 1)
    data = data[pd.notna(data['price'])]
    data['popularity'] = pd.to_numeric(data['popularity'])

    # sort by reference
    if preference == 'ratings' :
        data = data.sort_values(by ='rating', ascending = False)        
    elif preference == 'popularity':
        data = data.sort_values(by ='popularity', ascending = False)
    else:
        data = data.sort_values(by = 'price', ascending = False)
     
    # filter top sorting result
    if category.lower() == 'hotel':
        selected_data = data.iloc[0:(days*3):]
    else:
        selected_data = data.iloc[0:(days*2*3):]

    return selected_data



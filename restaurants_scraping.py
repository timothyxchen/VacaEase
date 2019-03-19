# -*- coding: utf-8 -*-

import requests
import pandas as pd


from urllib.parse import quote


# This class will call Yelp API and scrap restaurants data to a dataframe
API_KEY = "XIWdsq3lCIlrtrrq__A5gFXSZNbgQDvui0EH4L9bLcDspU5aFkvRJx-ylf9abKG9zN8ZFsDYPPtALxZCYQF" \
          "-ov_s6zzv6McClml3JNo3NLNaDxsyreLofbREL8FHXHYx "
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
SEARCH_LIMIT = 50

# request method to send http request to yelp
def request(host, path, api_key, url_params=None):

    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


# search method to set all parameters
def search(api_key, term, location, price, sort_by):

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        # Pricing levels to filter the search result with: 1 = $, 2 = $$, 3 = $$$, 4 = $$$$.
        # The price filter can be a list of comma delimited pricing levels.
        # For example, "1, 2, 3" will filter the results to show the ones that are $, $$, or $$$.
        'price': price,
        # best_match, rating, review_count or distance
        'sort_by': sort_by
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


# initial method to start scarping process
def scrap(location, search_term="restaurant", price=None, sort_by=None):
    # make api search request
    response = search(API_KEY, search_term, location, price, sort_by)
    clean_result = {}
    for result in response.get("businesses"):
        phone = result.get("phone")[2:]
        formatted_phone = ""
        for i in range(len(phone)):
            if i == 3 or i == 6:
                formatted_phone += "-"
            formatted_phone += phone[i]
        clean_result[result.get("name")] = [result.get("name"),
                                            ", ".join(result.get("location").get("display_address")),
                                            result.get("rating"),
                                            result.get("review_count"),
                                            result.get("price"),
                                            ", ".join([category.get("title") for category in result.get("categories")]),
                                            result.get("url"),
                                            result.get("image_url"),
                                            formatted_phone,
                                            ""]
    #     .replace(",", "-") + result.get("phone")[-1]
    columns = ["Name", "address", "rating", "popularity", "price", "category", "url", "imageurl", "phone", "description"]
    df = pd.DataFrame.from_dict(data=clean_result, orient="index",columns=columns)
    return df


if __name__ == '__main__':
    scrap("Pittsburgh")

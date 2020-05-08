import json
import requests
import sys

import pandas as pd

with open('secret.txt', 'r') as f:
    API_KEY = str(f.readline())

    url = 'https://maps.googleapis.com/maps/api/place/details/json?'\
        'place_id={place_id}&fields=name,rating,formatted_phone_number,reviews'\
        '&key={API_KEY}'.format(place_id=str(sys.argv[1]), API_KEY=API_KEY)
    x = requests.get(url)
    response = x.json()

    # the json file where the output must be stored  
    out_file = open("data/response.json", "w")
    json.dump(response, out_file, indent = 6)
    out_file.close()

    # saving reviews
    reviews = pd.DataFrame(response['result']['reviews'])
    reviews['time_stamp'] = pd.to_datetime(reviews.time, unit = 's')
    reviews['time_stamp'] = pd.DataFrame(pd.DatetimeIndex(
        reviews.time_stamp.dt.tz_localize('UTC')).tz_convert('Asia/Kolkata'))
    reviews.to_csv('data/reviews.csv', index = False)
    print(reviews)
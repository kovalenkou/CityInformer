# Find information about the country, currency and population of the city name
# Countries & Cities API - https://countriesnow.space/api/v0.1/
import argparse

import requests


def country_info(item):
    city = ''
    country = ''
    currency = ''
    population = ''
    for key, value in item.items():
        if key == 'city':
            city = value
        elif key == 'country':
            country = value
            # call
            currency = 'UAH'
        elif key == 'populationCounts':
            population = value[0]['value']
    msg_template = f"{'-' * 25}\n{city}\n\n{country}\n{currency}\n{population}\n{'=' * 25}"
    return msg_template


base_url = "https://countriesnow.space/api/v0.1/"
single_city_url = base_url + "countries/population/cities"
cities_from_country_url = base_url + "countries/population/cities/filter"

# url = cities_from_country_url if 1 == 1 else single_city_url
# response = requests.post(url, json={'city': 'kiev'})

response = requests.post(single_city_url, json={'city': 'Odessa'})
results = response.json()
print(country_info(results['data']))

# response = requests.get(single_city_url)
# results = response.json()
# for result in results['data']:
#     print(country_info(result))

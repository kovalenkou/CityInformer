# CityInformer project
import argparse

import requests


class CityInformer:
    """
    Find information about the city, country, currency and population:
     - by the city name (single output);
     - by the country name (multiply output).
    Countries & Cities API - https://countriesnow.space/api/v0.1/
    """

    _BASE_URL = "https://countriesnow.space/api/v0.1/"
    _SINGLE_CITY_URL = _BASE_URL + "countries/population/cities"
    _CITIES_FROM_COUNTRY_URL = _BASE_URL + "countries/population/cities/filter"
    _CURRENCY_FROM_COUNTRY_URL = _BASE_URL + "countries/currency"

    def __init__(self, search_name, info_type):
        self._search_name = search_name
        self._info_type = info_type

    def info_request(self):
        """
        API-request by the object params
        :return: NONE
        """
        if self._info_type == 'city':
            response = requests.post(self._SINGLE_CITY_URL, json={'city': f'{self._search_name}'})
            results = response.json()
            if results['error']:
                print(self.msg_error(f'Invalid name: {self._search_name}'))
            else:
                print(self._country_info(results['data']))
        elif self._info_type == 'country':
            response = requests.post(self._CITIES_FROM_COUNTRY_URL,
                                     json={
                                         'limit': 100,
                                         'order': 'asc',
                                         'orderBy': 'name',
                                         'country': f'{self._search_name}'
                                     }
                                     )
            results = response.json()
            if results['error']:
                print(self.msg_error(f'Invalid name: {self._search_name}'))
            else:
                for result in results['data']:
                    print(self._country_info(result))
        else:
            print(self.msg_error('Type input error'))

    def _currency_request(self, country_name):
        """
        API-request for currency info by country name
        :param country_name: country name
        :return: currency code
        """
        results = requests.post(self._CURRENCY_FROM_COUNTRY_URL, json={'country': f'{country_name}'}).json()
        return str(results['data']['currency'])

    def _country_info(self, item):
        """
        Formats string with city, country, currency and population information
        :param item: object with information
        :return: formatted text
        """
        city = item['city']
        country = item['country']
        currency = self._currency_request(country)
        population = item['populationCounts'][0]['value']
        msg_template = f"{'-' * 25}\n{city}\n\n{country}\n{currency}\n{population}\n{'=' * 25}"
        return msg_template

    @staticmethod
    def msg_error(text):
        """
        Formats string for error text
        :param text: error message
        :return: formatted text
        """
        return f"{'-' * 25}\n{text}\n{'=' * 25}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process to get info from request the city or country name.')
    # Some problems in API, that not fine search the names
    parser.add_argument('type', default='city', choices=['city', 'country'],
                        help='Type of search: "city" or "country" only allowed')
    # for names with two words
    parser.add_argument('name', nargs='+', help='Name for the search')

    args = parser.parse_args()
    name = ' '.join(args.name)
    city_info = CityInformer(name, args.type)
    try:
        city_info.info_request()
    except SystemError as error:
        print(CityInformer.msg_error('System error'))

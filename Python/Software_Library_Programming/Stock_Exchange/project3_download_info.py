import json
import urllib.parse
import urllib.request
import urllib.error


# base url
BASE_IEX_URL = 'https://api.iextrading.com/1.0/stock/market'


'''Determines the range of data needed to gather'''
def _time_period(days: int) -> str:

    timePeriod = ''

    # period of data
    if 0 < days <= 20:
        timePeriod = '1m'
    elif 20 < days <= 60:
        timePeriod = '3m'
    elif 60 < days <= 120:
        timePeriod = '6m'
    elif 120 < days <= 240:
        timePeriod = '1y'
    elif 240 < days <= 480:
        timePeriod = '2y'
    elif 480 < days <= 999:
        timePeriod = '5y'

    return timePeriod


'''constructs the url for search'''
def build_search_url(stock_symbol: str, days: int) -> str:

    timePeriod = _time_period(days)

    # parameters
    query_parameters = [
        ('symbols', stock_symbol),
        ('types', 'stats chart'),
        ('range', timePeriod)
    ]

    parameters = urllib.parse.urlencode(query_parameters)
    # changes unique symbol back to comma for parameter use in url
    parameters = parameters.replace('+' , ',')

    return BASE_IEX_URL + '/batch?' + parameters


'''
Requests information from url and opens it
Reads the inforamtion that was open and decodes it into json text
Allows user to access this information
'''
def request_stock_info(url: str) -> dict:

    # requests a the url
    response = urllib.request.urlopen(url)

    # reads the data
    data = response.read()

    # closes the object after finished using
    response.close()

    # decodes the information
    json_text = data.decode(encoding = 'utf-8')

    # loads as string, creates dictionary
    return json.loads(json_text)
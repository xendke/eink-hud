import os
import socket
import logging

from datetime import datetime
from newsapi import NewsApiClient
from pyowm.owm import OWM
from dotenv import load_dotenv
from const import WEATHER_COUNT

load_dotenv()
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')

def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

WEATHER_ICONS = {
    '01d': 'b',
    '02d': 'c',
    '03d': 'f',
    '04d': 'f',
    '09d': 'g',
    '10d': 'g',
    '11d': 'j',
    '13d': 'n',
    '50d': 'o'
}

SOURCES = ','.join(['abc-news','al-jazeera-english','ars-technica','associated-press','axios','bloomberg','breitbart-news','business-insider','cbs-news','cnn','crypto-coins-news','engadget','fortune','fox-news','google-news','hacker-news','medical-news-today','msnbc','national-geographic','national-review','nbc-news','new-scientist','newsweek','new-york-magazine','next-big-future','politico','recode','reddit-r-all','reuters','techcrunch','techradar','the-american-conservative','the-hill','the-huffington-post','the-next-web','the-verge','the-wall-street-journal','the-washington-post','the-washingjton-times','time','usa-today','vice-news','wired'])

def get_date():
    return datetime.now().strftime("%m/%d")
    
def get_time():
    return datetime.now().strftime("%I:%M%p")

def fetch_news_mock():
    return ['mock news ..', 'mock news ..', 'mock news ..']


news_api = NewsApiClient(NEWS_API_KEY)

def fetch_news():
    try:
        def trim_title(title):
            truncated = title[:180] + (title[180:] and '..')
            return truncated
        response = news_api.get_top_headlines(sources=SOURCES, page_size=30)
        result = [trim_title(article['title']) for article in response['articles']]
        return result
    except:
        logging.exception('news api failed')
        return fetch_news_mock()


def fetch_weather_mock():
    mock = []
    for _ in range(0, WEATHER_COUNT):
        mock.append({'temp': '00', 'icon': 'b', 'label': 'Sun'})
    return mock

open_weather_map = OWM(WEATHER_API_KEY)
weather_api = open_weather_map.weather_manager()

def fetch_weather():
    try: 
        one_call = weather_api.one_call(lat=41.032730, lon=-73.766327, exclude='minutely,hourly')

        result = []
        for i in range(0, WEATHER_COUNT):
            day = {}
            temp = one_call.forecast_daily[i].temperature('fahrenheit').get('feels_like_day', None)
            week_day = datetime.fromtimestamp(one_call.forecast_daily[i].reference_time()).strftime("%a")
            day['temp'] = str(round(temp))
            day['label'] = week_day.upper()
            day['icon'] = WEATHER_ICONS[one_call.forecast_daily[i].weather_icon_name]
            result.append(day)

        return result
    except:
        logging.exception('weather api failed')
        return fetch_weather_mock()

def with_interval(current):
    def every(interval):
        unit = interval[-1]
        amount = int(interval[:-1])
        if unit == 'h':
            amount = amount * 60
        elif unit == 'm':
            amount = amount * 1
        else:
            amount = amount
        
        return current % amount == 0
    return every

import os
import socket
from datetime import datetime
from newsapi import NewsApiClient # type: ignore
from pyowm.owm import OWM # type: ignore
from dotenv import load_dotenv # type: ignore

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

def fetch_news():
    def trim_title(title):
        truncated = title[:90] + (title[90:] and '..')
        return truncated
    api = NewsApiClient(NEWS_API_KEY)
    response = api.get_top_headlines(sources=SOURCES, page_size=3)
    result = [trim_title(article['title']) for article in response['articles']]
    return result


def fetch_weather_mock():
    return [{'temp': '56', 'icon': 'b', 'label': 'Sun'}, {'temp': '59', 'icon': 'c', 'label': 'Mon'}, {'temp': '60', 'icon': 'f', 'label': 'Tue'}]

def fetch_weather():
    owm = OWM(WEATHER_API_KEY)
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=41.032730, lon=-73.766327, exclude='minutely,hourly')

    result = []
    for i in range(0,3):
        day = {}
        temp = one_call.forecast_daily[i].temperature('fahrenheit').get('feels_like_day', None)
        week_day = datetime.fromtimestamp(one_call.forecast_daily[i].reference_time()).strftime("%a")
        day['temp'] = str(round(temp))
        day['label'] = week_day.upper()
        day['icon'] = WEATHER_ICONS[one_call.forecast_daily[i].weather_icon_name]
        result.append(day)

    return result

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

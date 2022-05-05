import os
import textwrap

from utils import get_date, get_time, fetch_news, fetch_weather
from assets import font_square, font_weather, font_small, font_smallest
from const import HEIGHT, WIDTH

# colors
black = 0
white = 255

def draw_news(draw, index = 0, cache = None):
    current_news = cache if cache else fetch_news() 
    draw.rectangle((129, 4, 246, 100), fill = black)
    single_news = "\n".join(textwrap.wrap(current_news[index], width=18))
    draw.multiline_text((188, 50), single_news, font = font_smallest, fill = white, anchor = "mm")
    return current_news

def draw_weather(draw):
    forecast = fetch_weather()
    draw.rectangle((7, 25, 127, 98), fill = white)
    x_coords = [30, 66, 103]
    for i in range(0,3):
        draw.text((x_coords[i], 40), forecast[i]['label'], font = font_small, fill = black, anchor = 'ms')
        draw.text((x_coords[i], 87), forecast[i]['icon'], font = font_weather, fill = black, anchor = 'ms')
        draw.text((x_coords[i], 92), forecast[i]['temp'], font = font_small, fill = black, anchor = 'ms')

def draw_date(draw):
    date = get_date()
    draw.rectangle((6, WIDTH-19, 100, WIDTH-19), fill = black)
    draw.text((6, WIDTH-19), date, font = font_square, fill = white)
    return date

def draw_time(draw):
    time = get_time()
    draw.rectangle((HEIGHT-65, WIDTH-19, HEIGHT-4, WIDTH-4), fill = black)
    draw.text((HEIGHT-6, WIDTH-19), time, font = font_square, fill = white, anchor = "ra")
    return time

import os
import logging
import time
from lib.waveshare_epd import epd2in13 # type: ignore
from PIL import Image, ImageDraw # type: ignore

from utils import get_date, get_time, with_interval # type: ignore
from draw import draw_news, draw_weather, draw_time, draw_date, font_square, white, black # type: ignore
from assets import background # type: ignore
from const import HEIGHT, WIDTH # type: ignore

logging.basicConfig(level=logging.DEBUG)

def main_screen(epd):
    canvas = Image.new('1', (HEIGHT, WIDTH), white)
    canvas.paste(background, (0,0))

    draw = ImageDraw.Draw(canvas)
    
    draw.text((7,7), 'Weather', font = font_square, fill = black)

    draw_weather(draw)

    previous_date = draw_date(draw)
    previous_time = draw_time(draw)

    news = draw_news(draw)

    epd.display(epd.getbuffer(canvas)) 

    iteration = 1
    while (True):
        every = with_interval(iteration)
        time_now = get_time()
        date_now = get_date()
        updated = False
        partial = True

        if(every('1h')):
            news = draw_news(draw)
            updated = True
            partial = False
        elif(every('10m')):
            draw_news(draw, iteration % len(news), news)
            updated = True

        if(every('6h')):
            draw_weather(draw)
            updated = True
            partial = False

        if(date_now != previous_date):
            previous_date = draw_date(draw)
            updated = True

        if(time_now != previous_time):
            previous_time = draw_time(draw)
            updated = True

        if(updated):
            if(partial):
                epd.init(epd.lut_partial_update)
            else:
                epd.init(epd.lut_full_update)
            epd.display(epd.getbuffer(canvas))

        iteration = iteration + 1

        time.sleep(60)

if __name__ == '__main__':
    try:
        logging.info("Starting...")
        
        epd = epd2in13.EPD()
        logging.info("Clearing Screen...")
        epd.init(epd.lut_full_update)
        epd.Clear(0x00)

        main_screen(epd)
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("Exiting...")
        epd2in13.epdconfig.module_exit()
        exit()

import logging
import time
from lib.waveshare_epd import epd2in13
from PIL import Image, ImageDraw

from utils import get_date, get_time, with_interval
from draw import draw_news, draw_weather, draw_time, draw_date, font_square, white, black
from assets import background
from const import HEIGHT, WIDTH

logging.basicConfig(
    filename='/home/pi/eink.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

def main_screen(epd):
    iteration = 0
    initiated = False
    while (True):
        if(not initiated):
            epd.init(epd.lut_full_update)
            epd.Clear(0x00)

            canvas = Image.new('1', (HEIGHT, WIDTH), white)
            canvas.paste(background, (0,0))

            draw = ImageDraw.Draw(canvas)
            
            draw.text((7,7), 'Weather', font = font_square, fill = black)

            draw_weather(draw)

            previous_date = draw_date(draw)
            previous_time = draw_time(draw)

            news = draw_news(draw)

            epd.display(epd.getbuffer(canvas))
            epd.sleep()
            time.sleep(60)
            initiated = True
            
            continue

        iteration = iteration + 1
        every = with_interval(iteration)

        time_now = get_time()
        date_now = get_date()
        updated = False
        partial = True

        if(every('12h')):
            news = draw_news(draw)
            updated = True
            partial = False
        elif(every('5m')):
            draw_news(draw, iteration % len(news), news)
            updated = True
            if(every('20m')):
                partial = False

        if(every('3h')):
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
            epd.sleep()


        time.sleep(60)

if __name__ == '__main__':
    try:
        logging.info("Starting...")
        
        epd = epd2in13.EPD()
        logging.info("Clearing Screen...")

        main_screen(epd)
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("Exiting...")
        epd2in13.epdconfig.module_exit()
        exit()

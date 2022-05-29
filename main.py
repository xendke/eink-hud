import logging
import time
from lib.waveshare_epd import epd2in13
from PIL import Image, ImageDraw

from utils import get_date, get_time, with_interval
from draw import draw_news, draw_weather, draw_time, draw_date, font_square, white, black
from assets import background_full
from const import HEIGHT, WIDTH

logging.basicConfig(
    filename='/home/pi/eink.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

def render_weather(epd, iteration):
    epd.init(epd.lut_full_update)
    epd.Clear(0x00)

    canvas = Image.new('1', (HEIGHT, WIDTH), white)
    canvas.paste(background_full, (0,0))

    draw = ImageDraw.Draw(canvas)
    
    draw.text((7,7), 'Weather', font = font_square, fill = black)

    draw_weather(draw)

    previous_date = draw_date(draw)
    previous_time = draw_time(draw)

    epd.display(epd.getbuffer(canvas))
    epd.sleep()
    time.sleep(60)

    def update():
        nonlocal previous_date
        nonlocal previous_time
        every = with_interval(iteration)

        time_now = get_time()
        date_now = get_date()
        updated = False
        partial = True

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
    return update

def render_news(epd, iteration):
    epd.init(epd.lut_full_update)
    epd.Clear(0x00)

    canvas = Image.new('1', (HEIGHT, WIDTH), white)
    canvas.paste(background_full, (0,0))

    draw = ImageDraw.Draw(canvas)
    
    draw.text((7,7), 'News', font = font_square, fill = black)

    previous_date = draw_date(draw)
    previous_time = draw_time(draw)

    news = draw_news(draw)

    epd.display(epd.getbuffer(canvas))
    epd.sleep()
    time.sleep(60)

    def update():
        nonlocal previous_date
        nonlocal previous_time
        nonlocal news
        every = with_interval(iteration)

        time_now = get_time()
        date_now = get_date()
        updated = False
        partial = True

        if(every('6h')):
            news = draw_news(draw)
            updated = True
            partial = False
        elif(every('2m')):
            draw_news(draw, iteration % len(news), news)
            updated = True

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
    return update

def render_loop(epd):
    global_iteration = 0

    all_screens = [{
        'name': 'weather',
        'iteration': 0,
        'initiated': False
    }, {
        'name': 'news',
        'iteration': 0,
        'initiated': False
    }]
    current_index = 0
    current_screen = all_screens[current_index]

    renderer = None
    while (True):
        every = with_interval(global_iteration)
        global_iteration = global_iteration + 1
        current_screen['iteration'] = current_screen['iteration'] + 1

        current = current_screen.get('name')
        initiated = current_screen.get('initiated')
        iteration = current_screen.get('iteration')

        if(current == 'weather'):
            if(initiated):
                renderer()
            else:
                renderer = render_weather(epd, iteration)
                current_screen['initiated'] = True

        
        if(current == 'news'):
            if(initiated):
                renderer()
            else:
                renderer = render_news(epd, iteration)
                current_screen['initiated'] = True

        if(every('10m')):
            current_screen['initiated'] = False
            current_index = (current_index + 1) % len(all_screens)
            current_screen = all_screens[current_index]
            current_screen['initiated'] = False

        
        

if __name__ == '__main__':
    try:
        logging.info("Starting...")
        
        epd = epd2in13.EPD()
        logging.info("Clearing Screen...")

        render_loop(epd)
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("Exiting...")
        epd2in13.epdconfig.module_exit()
        exit()

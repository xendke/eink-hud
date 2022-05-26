import os
import logging

from PIL import Image, ImageFont

assets_dir = os.path.dirname(os.path.realpath(__file__))

background = Image.open(os.path.join(assets_dir, 'background.bmp'))
logging.info("assets/__init__.py executed")

font_square = ImageFont.truetype(os.path.join(assets_dir, 'Square.ttf'), 15)
font_weather = ImageFont.truetype(os.path.join(assets_dir, 'Weather.ttf'), 50)
font_small = ImageFont.truetype(os.path.join(assets_dir, 'Small.ttf'), 14)
font_smallest = ImageFont.truetype(os.path.join(assets_dir, 'Smallest.ttf'), 14)

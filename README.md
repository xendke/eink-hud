# Weather, News and More on eInk Display
A HUD script written in Python to display weather, news, datetime etc...

![Screenshot of HUD](/hud.jpeg)

## Prerequisites

I am running this on a Raspberry Pi Zero W running Raspberry Pi OS Lite (buster). The display is a Waveshare 2.13in ePaper HAT attached via the GPIO pins to the Pi.

[Docs](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT#Users_Guides_of_Raspberry_Pi) on getting started with the display. Once the provided `example.py` script was working correctly, I used it as a guide for my project.

Other Python dependencies:
```
- Pillow
- newsapi-python
- pyowm
- dotenv
```

## Running the script
```
python3 main.py
```

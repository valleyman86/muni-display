import sys
import os
from PIL import Image
sys.path.append(os.path.expanduser('~/Documents/e-Paper/RaspberryPi_JetsonNano/python/lib'))  # path to the driver folder

from waveshare_epd import epd7in5_V2

def display_image(image_path):
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    # Load and convert the image
    image = Image.open(image_path)
    image = image.resize((800, 480))  # Adjust to your model's resolution
    epd.display(epd.getbuffer(image))

    epd.sleep()
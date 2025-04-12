import sys
import os
from PIL import Image
sys.path.append(os.path.expanduser('~/Documents/e-Paper/RaspberryPi_JetsonNano/python/lib'))  # path to the driver folder

from waveshare_epd import epd7in5_V2


def init_epd():
    """
    Initializes the 7.5" Waveshare e-ink display and returns the epd object.
    Only call this once to avoid repeated slow startups.
    
    :return: Initialized EPD object
    """
    epd = epd7in5_V2.EPD()
    epd.init()
    print("🖥️ EPD initialized")
    return epd

def display_image(epd, image):
    """
    Displays a PIL image directly on a 7.5" Waveshare e-ink display (800x480).
    
    :param image: PIL.Image.Image object
    """
    try:
        # epd = epd7in5_V2.EPD()
        # epd.init()
        #epd.Clear()

        # Ensure correct size and mode
        image = image.rotate(90, expand=True)
        image = image.resize((800, 480)).convert("1", dither=Image.NONE)

        epd.display(epd.getbuffer(image))
        #epd.sleep()
        print("🖼️ Image displayed on e-ink screen")

    except Exception as e:
        print(f"❌ Failed to display image: {e}")
import time 
from datetime import datetime
from zoneinfo import ZoneInfo
from jinja2 import Environment, FileSystemLoader
from muni import *
from utils import *
import platform

# Detect if running on a Raspberry Pi (and not macOS)
on_raspberry_pi = platform.system() == "Linux"

print(platform.system())
print(platform.machine())
print(platform.uname().node.lower())

if on_raspberry_pi:
    from einkUtils import *

    epd = init_epd()

# Example usage of the function
STOP_ID_L_OWL_WESTBOUND = '16616'
STOP_ID_L_OWL_EASTBOUND = '16617'
STOP_ID_28_NORTHBOUND = '13394'
STOP_ID_28_SOUTHBOUND = '13395'

def main():
    # Set up Jinja environment (template folder = current directory)
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('hello.html')

    pacific_now = datetime.now(ZoneInfo("America/Los_Angeles"))
    current_time = pacific_now.strftime("%-I:%M %p") # e.g., 3:45 PM

    # render muni stop
    formattedTimes = {
        # "times_L_zoo": get_formatted_arrival_times(get_muni_stop_data(STOP_ID_L_OWL_WESTBOUND)),
        "times_L_em": get_formatted_arrival_times(get_muni_stop_data(STOP_ID_L_OWL_EASTBOUND)),
        "times_28_fw": get_formatted_arrival_times(get_muni_stop_data(STOP_ID_28_NORTHBOUND)),
        # "times_28_dc": get_formatted_arrival_times(get_muni_stop_data(STOP_ID_28_SOUTHBOUND)),
        "current_time": current_time  
    }

    # formattedTimes = {
    #     "times_28_fw": "3, 6, 9",
    #     "times_28_dc": "2🚀, 5, 10🚀",
    #     "times_L_em": "1🦉,7,13🦉",
    #     "times_L_zoo": "4,8,12"
    # }

    # Enable debug mode if not on a Pi
    debug = not on_raspberry_pi

    image = render_muni_times_to_html(formattedTimes, debug=debug)

    if on_raspberry_pi and image:
        display_image(epd, image)

# Loop forever on Pi, just once otherwise
if on_raspberry_pi:
    while True:
        main()
        time.sleep(65)
else:
    main()
    print("Program Finished")
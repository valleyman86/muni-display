import os
import requests
import json
from types import SimpleNamespace
from utils import *

muniApiKey = os.getenv("MUNI_API_KEY")

def get_muni_stop_data(stop):
    url = (
        f"https://api.511.org/transit/StopMonitoring?"
        f"api_key={muniApiKey}&agency=SF&stopcode={stop}&format=json&MaximumStopVisits=10"
    )
    
    try:
        response = requests.get(url, timeout=10)  # Timeout is optional but recommended
        response.raise_for_status()  # Raise an error for HTTP 4xx/5xx
        response_text = response.content.decode('utf-8-sig')
        posts = json.loads(response_text, object_hook=lambda d: SimpleNamespace(**d))
        return posts

    except requests.exceptions.RequestException as e:
        print(f"Network error when fetching stop {stop}: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON parsing error for stop {stop}: {e}")
    except Exception as e:
        print(f"Unexpected error for stop {stop}: {e}")

    return None
    
def get_formatted_arrival_times(stops, max_visits=3):
    """
    Formats arrival times from Muni stop data.
    Adds 🦉 for OWL lines or LineRef '91', 🚀 for express 'R' lines (first/last only).
    No 'min' or parentheses. Comma-separated with space.

    Returns:
        A string like "2🚀, 5, 10🦉" or "3, 6, 9"
    """
    if not stops:
        print("No stop data received.")
        return "No arrivals"

    visits = stops.ServiceDelivery.StopMonitoringDelivery.MonitoredStopVisit[:max_visits]
    arrival_entries = []

    for i, visit in enumerate(visits):
        try:
            minutes = time_until_utc_min(visit.MonitoredVehicleJourney.MonitoredCall.ExpectedArrivalTime)
            line = visit.MonitoredVehicleJourney.LineRef.upper()

            show_line = (line == "91" or "R" in line or "OWL" in line) and (i == 0 or i == len(visits) - 1)

            if show_line:
                if "OWL" in line or line == "91":
                    minutes = f"{minutes}🦉"
                elif "R" in line:
                    minutes = f"{minutes}🚀"

            arrival_entries.append(str(minutes))

        except Exception as e:
            print(f"Skipping visit due to error: {e}")

    return ", ".join(arrival_entries) if arrival_entries else "No arrivals"

def render_muni_times_to_html(formattedTimes, template_name='hello.html', debug=False):
    """
    Renders Muni times into HTML and passes to image renderer.

    :param formattedTimes: dict of data to render into template
    :param template_name: Jinja template file
    :param debug: If True, saves rendered HTML and BMP image to disk
    :return: PIL.Image.Image object or None
    """
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    html_output = template.render(**formattedTimes)

    if debug:
        with open("hello-out.html", "w") as f:
            f.write(html_output)
        print("📝 Saved debug HTML: hello-out.html")

    print("🧠 Rendered HTML context:", formattedTimes)

    # Convert to image in-memory
    return convert_html_to_image_weasy(html_output, debug=debug)
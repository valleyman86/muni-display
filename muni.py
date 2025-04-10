import requests
import json
from types import SimpleNamespace
from utils import *

muniApiKey = "82491e7f-0a68-47fe-8284-43da4048c499"

def get_muni_stop_data(stop):
    # Construct the API URL
    url = f"https://api.511.org/transit/StopMonitoring?api_key={muniApiKey}&agency=SF&stopcode={stop}&format=json&MaximumStopVisits=10"
    
    # Send GET request to the API
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code == 200:
        # Parse JSON data
        response_text = response.content.decode('utf-8-sig')
        posts = json.loads(response_text, object_hook=lambda d: SimpleNamespace(**d))
        
        # Return the parsed data
        return posts
    else:
        print(f"Failed to retrieve data: {response.status_code}")
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
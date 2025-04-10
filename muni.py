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

def render_muni_times_to_html(formattedTimes, output_html='hello-out.html', template_name='hello.html'):
    # Set up Jinja2 environment and render
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    output = template.render(**formattedTimes)

    #todo Joey: Do not save the html unless in a debug state and try to just use memory    
    with open(output_html, "w") as f:
        f.write(output)

    print("Rendered HTML:", formattedTimes)

    # Convert to image
    convert_html_to_image_weasy(output_html)
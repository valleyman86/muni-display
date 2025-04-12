import pytz
import io
from datetime import datetime
from html2image import Html2Image
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from weasyprint import HTML
from PIL import Image
from pdf2image import convert_from_bytes

def convert_to_pst(time):
    """
    Converts the ISO 8601 formatted time string to a human-readable time in PST.
    
    Parameters:
    - time: The ISO 8601 formatted time string (e.g. '2025-04-08T08:50:16Z')
    
    Returns:
    - A string representing the time in PST (e.g. '2025-04-08 01:50:16 AM PDT')
    """
    # Convert the string to a datetime object (assuming the format is ISO 8601)
    time_dt = datetime.fromisoformat(time.replace("Z", "+00:00"))  # Adjusting if 'Z' for UTC is present

    # Check if the datetime is naive (no tzinfo) or aware (has tzinfo)
    if time_dt.tzinfo is None:
        # If naive, localize it to UTC
        time_dt = pytz.utc.localize(time_dt)
    else:
        # If aware, it's already in a timezone, so no need to localize
        pass

    # Convert to PST (Pacific Standard Time)
    pst_zone = pytz.timezone('US/Pacific')
    time_pst = time_dt.astimezone(pst_zone)

    # Format the time for human readability
    human_readable_time = time_pst.strftime('%Y-%m-%d %I:%M:%S %p %Z')

    return human_readable_time

def time_until_utc(utc_date_str):
    # Parse the UTC date string into a datetime object
    utc_date = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
    
    # Get the current UTC time
    current_time = datetime.utcnow()
    
    # Calculate the time difference
    time_diff = utc_date - current_time
    
    # Get the number of days, hours, minutes, and seconds
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Build the result with non-zero parts
    time_parts = []
    if days > 0:
        time_parts.append(f"{days} days")
    if hours > 0:
        time_parts.append(f"{hours} hours")
    if minutes > 0:
        time_parts.append(f"{minutes} minutes")
    if seconds > 0:
        time_parts.append(f"{seconds} seconds")
    
    # Join the non-zero parts with commas
    return ', '.join(time_parts)

# Helper: convert UTC string to minutes from now
def time_until_utc_min(utc_str):
    dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
    delta = dt - datetime.utcnow()
    return max(0, int(delta.total_seconds() // 60))  # never return negative

# doesn't really work on pi zero with <1gb ram
def html_to_image_with_chromium_from_file(html_file_path, output_image='hello.png'):
    hti = Html2Image(browser_executable=None)
    
    # Use new headless mode for compatibility with latest Chromium
    hti.browser.flags.append("--headless=new")
    hti.browser.flags.append("--disable-gpu")

    # Render and save image
    hti.screenshot(
        html_file=html_file_path,
        save_as=output_image,
        size=(800, 480)
        # size=(480, 800)
    )

    image = Image.open(output_image).convert('1', dither=Image.NONE)
    image.save('hello.bmp')

from weasyprint import HTML
from PIL import Image
from pdf2image import convert_from_bytes

def convert_html_to_image_weasy(html_content, debug=False, debug_path="hello-out"):
    """
    Converts raw HTML content to a Pillow image using WeasyPrint and pdf2image.

    :param html_content: HTML as a string
    :param debug: If True, saves the output BMP image
    :param debug_path: Base name used for debug image file
    :return: PIL.Image.Image object or None on failure
    """
    try:
        # Convert HTML string to PDF bytes in memory
        pdf_bytes = HTML(string=html_content).write_pdf()

        # Convert PDF to image
        images = convert_from_bytes(pdf_bytes)
        if images:
            image = images[0].resize((480, 800)).convert("1", dither=Image.NONE)

            if debug:
                image.save(f"{debug_path}.bmp", format="BMP")
                print(f"🖼️  Saved debug BMP: {debug_path}.bmp")

            return image
        else:
            print("❌ No image rendered from HTML.")
            return None

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return None
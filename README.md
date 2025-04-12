# Muni Display

**Muni Display** is a Python-based application designed to fetch real-time San Francisco Muni transit data and display it on an e-ink screen. This project is ideal for Raspberry Pi setups with Waveshare displays, offering a low-power, always-on transit dashboard.

## Features

- Real-time Muni transit data  
- E-ink display rendering  
- HTML-to-image support  
- Lightweight and efficient  

## Usage

```bash
python3 main.py
```

Customize routes and stops in `muni.py`. Ensure your e-ink screen is connected and supported by the Waveshare driver.

## Project Structure

- `main.py` – App entry point  
- `muni.py` – Fetches and parses transit data  
- `einkUtils.py` – Handles e-ink display rendering  
- `utils.py` – HTML/image utilities  

## Requirements

```txt
requests
Pillow
RPi.GPIO
spidev
python-periphery
html2image
jinja2
weasyprint
pdf2image
pytz
waveshare-epd
```

## License

MIT License

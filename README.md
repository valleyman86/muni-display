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

Ensure your e-ink screen is connected and supported by the Waveshare driver.

## Customizing Stops

To add or remove stops from the display, you need to update both `main.py` and `hello.html`.

### ➕ Adding a Stop

#### 1. In `main.py`

Use the `get_formatted_arrival_times` function to populate a new stop:

```python
STOP_ID_5_MARKET = '12345'  # Replace with the actual stop ID

formattedTimes = {
    "times_L_em": get_formatted_arrival_times(get_muni_stop_data(STOP_ID_L_OWL_EASTBOUND)),
    "times_28_fw": get_formatted_arrival_times(get_muni_stop_data(STOP_ID_28_NORTHBOUND)),
    "times_5_mkt": get_formatted_arrival_times(get_muni_stop_data(STOP_ID_5_MARKET)),
    "current_time": current_time
}
```

#### 2. In `hello.html`

Add a new `<tr>` to the table:

```html
<tr>
  <td class="no-right-border">
    <div class="cell-content">
      <div class="circle"><span>5</span></div>
      <div class="text-block">
        <span class="destination">Market Street</span>
        <span class="times">{{ times_5_mkt }}</span>
      </div>
    </div>
  </td>
</tr>
```

Make sure the `{{ times_5_mkt }}` key matches the one in `formattedTimes`.

### ➖ Removing a Stop

1. Delete the corresponding key from `formattedTimes` in `main.py`.
2. Remove the associated row (`<tr>`) from `hello.html`.

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


---

🧠 **Note**: This project was created with approximately 99% help from AI (ChatGPT). 

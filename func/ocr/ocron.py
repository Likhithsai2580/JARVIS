from PIL import ImageGrab
import io
from time import sleep, time as t
import requests
import pyautogui as pag
C = t()

def ocr_on(search_string, url, double_click=False):
    screenshot = ImageGrab.grab()
    image_bytes = io.BytesIO()
    screenshot.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    if double_click:
        payload = {
            "search_string": search_string,
            "double_click": "on"
        }
    else:
        payload = {
            "search_string": search_string,
            "double_click": "off"
        }
    
    files = {'image': image_bytes}

    r = requests.post(url, files=files, data=payload)
    if "error" in r:
        return f"no button found named {search_string}"
    else:
        screenshot.close()
        print(t() - C)
        response = r.json()
        print(response["time"])
        point = response["point"]
        if double_click:
            pag.click(point)
            sleep(0.30)
            pag.click(point)
        else:
            pag.click(point)
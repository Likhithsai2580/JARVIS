#https://colab.research.google.com/drive/1xenMnAqGydJnsNV5C9aQ4ysrOCdNgXdf?usp=sharing

import cv2
import requests
import json
import time 
import base64
cache = {}

def url():
    try:
        # Check if URL exists in cache and is not expired
        if 'url' in cache and cache['url'][1] > time.time():
            return cache['url'][0]
        
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            url = config.get('camera')
            if url is None:
                raise ValueError("Img_Detection_Colab not found in config file")
            # Cache the URL with expiration time of 1 hour
            cache['url'] = url, time.time() + 3600
            return url
    except FileNotFoundError:
        print("Config file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON in config file.")
    except Exception as e:
        print(f"Error reading config file: {e}")

def capture_and_send_image():
    # URL of the FastAPI server endpoint
    api_url = url()

    # Replace this URL with your ngrok URL
    ngrok_url = f"{api_url}/stream"

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    if not ret:
        break

    # Encode frame to JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    # Send frame to server
    response = requests.post(ngrok_url, data={'image': jpg_as_text})
    
    if response.status_code == 200:
        print("Frame sent successfully")
        return response
    else:
        print("Failed to send frame")
    cap.release()
    cv2.destroyAllWindows()
    break


#https://colab.research.google.com/drive/1t1hYuKqQIyxuiBw2y6Ja66iNxa-nuCgK?usp=sharing
import cv2
import requests
import json
import time 
cache = {}
def url():
    try:
        # Check if URL exists in cache and is not expired
        if 'url' in cache and cache['url'][1] > time.time():
            return cache['url'][0]
        
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            url = config.get('Img_Detection_Colab')
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

    # Open the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Failed to open camera")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Failed to capture frame")
        return

    # Release the camera
    cap.release()

    # Prepare the payload
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'file': img_encoded.tobytes()}

    # Send a POST request to the server
    response = requests.post(api_url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        detections = result['detections']
        object_names = [obj['name'] for obj in detections[0] if obj['confidence'] > 0.5]  # Adjust confidence threshold as needed
        return("Detected objects:", object_names)
    else:
        # Print error message if request fails
        print("Error:", response.text)

    # Display the captured frame
    cv2.imshow('Captured Image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

from os import system, listdir
from PIL import Image
import os
import json

def cookie_bing():
    try:
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            gemini_api = config.get('cookie_bing')
            if gemini_api is None:
                raise ValueError("cookie_bing not found in config file")
            return gemini_api
    except FileNotFoundError:
        print("Config file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON in config file.")
    except Exception as e:
        print(f"Error reading config file: {e}")

cookie = cookie_bing()

def generate_images(prompt):
    # Enclose the prompt within quotes
    command = f"python -m BingImageCreator -U {cookie} --prompt \"{prompt}\""
    system(command)
    files = listdir("output")
    # Reverse the list of files and select the last four elements
    return files[-4:]

class ShowImage:
    def __init__(self, folder_path, files):
        self.folder_path = folder_path
        self.files = files

    def open(self, index):
        # Construct the absolute path to the image file
        img_path = os.path.join(self.folder_path, self.files[index])
        img = Image.open(img_path)
        img.show()

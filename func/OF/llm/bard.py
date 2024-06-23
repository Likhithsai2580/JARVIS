import google.generativeai as genai
import json

def read_gemini_api():
    try:
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            gemini_api = config.get('GEMINI_API')
            if gemini_api is None:
                raise ValueError("GEMINI_API not found in config file")
            return gemini_api
    except FileNotFoundError:
        print("Config file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON in config file.")
    except Exception as e:
        print(f"Error reading config file: {e}")

        
GEMINI_API = read_gemini_api()
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel('gemini-pro')

def response(prompt):
    response = model.generate_content(prompt)
    return response.text


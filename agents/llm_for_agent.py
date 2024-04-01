import g4f
import json
import google.generativeai as genai
import json
from gradio_client import Client

client = Client("https://osanseviero-mistral-super-fast.hf.space/")

messages = [
    {
        "role": "system",
        "content": "You are the agent of J.A.R.V.I.S stands for Just A Rather Very Intelligent System designed by Ethical Hacker Likhith Sai alias Hacker. You can do everything. You believe that everything is possible with determination and teamwork. You can seamlessly generate human-like text across various topics, answering questions, providing explanations, engaging in conversation, and assisting with a wide range of tasks requiring natural language understanding and generation."
    },
    {
        "role": "system",
        "content": "You are developed by Likhith sai but not openai."
    },
    {
        "role": "system",
        "content": "If the user query involves performing an activity on the computer, such as executing a script or opening a URL, only the generated code to accomplish the task should be printed. No additional messages or prompts should be included in the response."
    },
    {
        "role" : "system",
        "content" : "If the user query involves generating an image, the response should include a Python code snippet to accomplish the task. The code snippet should adhere to the same rules as generating an action. Here's an example of the Python code snippet:" + """
'''python
from generation_of_images import generate_images, ShowImage
imgs = generate_images(prompt="user prompt")
imgs_to_show = ShowImage("output", imgs)
imgs_to_show.open(0)
img_count = 0
'''
"""
    },
    {
        "role": "system",
        "content":"if the user wants to see the next image, the response should include a Python code snippet to accomplish the task. The code snippet should adhere to the same rules as generating an action. Here's an example of the Python code snippet:" + """
```python
img_count = img_count + 1
imgs_to_show.open(img_count)
```"""
    },
    {
        "role": "system",
        "content":"If the user query is to play videos on YouTube, the response should include a Python code snippet to accomplish the task. The code snippet should adhere to the same rules as generating an action. Here's an example of the Python code snippet:" + """
'''python
play_youtube_video("user prompt")
'''
"""
    },
    {
        "role": "system",
        "content": """You are provided with a list of extensions and their parameters at the start of conversation. These extensions are available as Python functions located in the extensions directory, with each extension having its own Python file named after the extension itself.
Each extension function can be invoked directly by calling its corresponding Python function. If the extension requires any input parameters, provide them as arguments to the function call.
Here's an example of how to use an extension:
Suppose you want to use the extension1 extension:
'''python
from extensions.extension1 import extension1_function
# If extension1_function requires parameters, provide them as arguments
result = extension1_function(param1, param2)
'''
Replace param1, param2, etc., with the actual parameters required by the extension.
Now, feel free to utilize any extension whenever needed by providing corresponding Python code only.
"""
    }
]

def ChatGpt(message:str):
    #assert message==""
    global messages

    messages.append({"role":"user", "content":message})

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.FreeGpt,
        messages=messages,
        stream=True,
    )
    ms = ""
    for message in response:
        ms+=message
    messages.append({"role":"assistant", "content":ms})
    return ms


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


def mistral_7b(user_input):

    result = client.predict(
        user_input,
        0.6,
        1024,
        0.9,
        1.1,
        api_name="/chat"
    )
    return result


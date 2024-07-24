import os
import sys
import json
import time  # Import time module for caching expiration
#from PyQt5 import QtWidgets, QtCore, QtGui
#from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread
#from PyQt5.QtWidgets import QApplication, QMainWindow
#from JarvisUi import Ui_JarvisUI
from func.basic.listenpy import Listen
from func.basic.chat import chat
from llm.chatgpt import ChatGpt
from llm.filter import filter
from llm.bard import response
from func.OF.dataonline import SearchTools
from func.OF.youtube import get_transcript_cached as get_transcript
from func.OF.youtube import transcription_cached as transcription
from func.Powerpointer.main import generate_powerpoint
from func.ocr.ocroff import ocr_off
from func.ocr.ocron import ocr_on
from func.speak.speakmid import mid as off
from func.speak.speakon import speak as on
import pywhatkit as kit
from os import system, listdir
from PIL import Image
import keyboard
import pyperclip
import socket
import threading
from agents.agent import start_work
import subprocess
import platform
from llm.localllm import locallm
from func.OF.obj_detect import capture_and_send_image

# Define a dictionary for caching
cache = {}
CACHE_EXPIRATION_TIME = 3600

def start_agent(work):
    start_work(work)

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server listening on {}:{}".format(host, port))
    
    while True:
        conn, addr = server_socket.accept()
        print("Connected by", addr)
        data = conn.recv(1024)
        if not data:
            break
        print("Received:", data.decode())
        on(ChatGpt(f"system: your agent gave this following data {data.decode()}"))
        conn.sendall(b"Message received")
        conn.close()

def get_os_info():
    # Check if OS info exists in cache
    if 'os_info' in cache:
        return cache['os_info']
    
    try:
        os_name = platform.system()
        if os_name == 'Linux':     
                dist_name, version, codename = platform.linux_distribution()
                os_info = f"Operating System: {os_name}\nDistribution: {dist_name}\nVersion: {version}\nCodename: {codename}"
        else:
            os_info = f"Operating System: {os_name}"
        
        # Cache the OS info with expiration time of 1 hour
        cache['os_info'] = os_info, time.time() + 3600
        return os_info
    except:
        os_name = platform.system()
        if os_name == 'Linux':
            try:
                with open('/etc/os-release', 'r') as file:
                    info = {}
                    for line in file:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            info[key] = value.strip('"')
                    os_info = f"Operating System: {os_name}\nDistribution: {info.get('NAME', 'Unknown')}\nVersion: {info.get('VERSION_ID', 'Unknown')}\nCodename: {info.get('VERSION_CODENAME', 'Unknown')}"
            except FileNotFoundError:
                os_info = f"Operating System: {os_name}\nDistribution: Unknown\nVersion: Unknown\nCodename: Unknown"
        else:
            os_info = f"Operating System: {os_name}"
        
        # Cache the OS info with expiration time of 1 hour
        cache['os_info'] = os_info, time.time() + 3600
        return os_info


def get_extension_info():
    # Check if extension info exists in cache
    if 'extension_info' in cache:
        return cache['extension_info']
    
    with open("extensions/config_all.json", 'r') as f:
        data = json.load(f)
    
    extensions_info = []
    for extension in data['extensions']:
        extension_info = {
            'name': extension['name'],
            'description': extension['description'],
            'parameters': extension['parameters']
        }
        extensions_info.append(extension_info)
    
    # Cache the extension info with expiration time of 1 hour
    cache['extension_info'] = extensions_info, time.time() + 3600
    return extensions_info


def exitTask():
    subprocess.Popen(["python", "app.py"])

def cookie_bing():
    # Check if Bing cookie exists in cache
    if 'bing_cookie' in cache:
        return cache['bing_cookie']
    
    try:
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            bing = config.get('cookie_bing')
            if bing is None:
                raise ValueError("cookie_bing not found in config file")
            # Cache the Bing cookie with expiration time of 1 hour
            cache['bing_cookie'] = bing, time.time() + 3600
            return bing
    except FileNotFoundError:
        print("Config file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON in config file.")
    except Exception as e:
        print(f"Error reading config file: {e}")

def generate_images(prompt):
    # Check if images for prompt exist in cache
    if prompt in cache:
        return cache[prompt]
    
    # Enclose the prompt within quotes
    command = f"python -m BingImageCreator -U {cookie_bing()} --prompt \"{prompt}\""
    system(command)
    files = listdir("output")
    # Reverse the list of files and select the last four elements
    images = files[-4:]
    
    # Cache the images for the prompt with expiration time of 1 hour
    cache[prompt] = images, time.time() + 3600
    return images

def play_youtube_video(video_query):
    try:
        kit.playonyt(video_query)
    except Exception as e:
        print("An error occurred:", str(e))


def url():
    try:
        # Check if URL exists in cache and is not expired
        if 'url' in cache and cache['url'][1] > time.time():
            return cache['url'][0]
        
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            url = config.get('OCR_Colab')
            if url is None:
                raise ValueError("OCR_Colab not found in config file")
            # Cache the URL with expiration time of 1 hour
            cache['url'] = url, time.time() + 3600
            return url
    except FileNotFoundError:
        print("Config file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON in config file.")
    except Exception as e:
        print(f"Error reading config file: {e}")


def execute_code(code):
    try:
        exec(code)
        return True, None
    except Exception as e:
        return False, e


def cached_function(key, func, *args, **kwargs):
    # Check if the result is cached and not expired
    if key in cache and cache[key]['expiration'] > time.time():
        return cache[key]['result']
    # Call the function and cache the result
    result = func(*args, **kwargs)
    cache[key] = {'result': result, 'expiration': time.time() + CACHE_EXPIRATION_TIME}
    return result

def execute_code_with_cache(code):
    # Cache the execution result based on code
    return cached_function(code, execute_code, code)

def process_voice_input(q):
    if any(keyword in q for keyword in ["bye", "see you later", "terminate"]):
        on("Bye sir, have a great day")
        exitTask()
        sys.exit()

    elif any(keyword in q for keyword in ["learn", "research"]):
        server_thread = threading.Thread(target=start_server, args=("127.0.0.1", "12345"))
        server_thread.start()
        q = q.lower().replace("research", "").replace("learn", "").replace("about", "")
        start_work(q)

    elif any(keyword in q for keyword in ["translate", "summarize", "transcribe"]):
        on("Please wait..")
        video_id = get_transcript()
        summary = transcription(video_id)
        off(ChatGpt(f"Summarize this transcription in points: {summary}"))

    elif any(keyword in q for keyword in ["powerpoint", "presentation"]):
        q = q.replace("create", "").replace("a", "").replace("powerpoint", "").replace("presentation", "").replace("on", "").replace("Create", "")
        os.startfile(generate_powerpoint(q))

    elif any(keyword in q for keyword in ["study", "this", "text", "code"]):
        keyboard.press_and_release("ctrl + c")
        clipboard = pyperclip.paste()
        query = q + clipboard + "if it needs to write on file use python code that tooo full code, do not write anything except code"
        rep = cached_function(query, ChatGpt, query)
        code = filter(rep)
        if code:
            success, error = execute_code_with_cache(code)
            if success:
                execute_code_with_cache(ChatGpt(f"You successfully completed the task for {q}. Respond for your successful completion."))
            else:
                off(f"Error executing code: {error}")
        else:
            off(rep)
    
    elif any(keyword in q for keyword in ["Jarvis", "jarvis"]):
        query = q + " ***Use Python programming language. Just write complete code nothing else***"
        rep = cached_function(query, ChatGpt, query)
        code = filter(rep) if rep else None
        if code:
            success, error = execute_code_with_cache(code)
            if success:
                on(ChatGpt(success))
                on(ChatGpt(f"You successfully completed the task for {q}. Respond for your successful completion."))
            else:
                off(f"Error executing code: {error}, code: {code}. Rewrite the full code, nothing else.")
        else:
            off("Sorry, I couldn't find any code to execute.")

    elif "click" in q:
        double_click = "double" in q
        q = q.replace("click", "").replace("on", "").replace("double", "").replace("jarvis", "")
        try:
            ocr_on(q, url=url(), double_click=double_click)
        except:
            ocr_off(q, double_click=double_click)

    else:
        chat_response = chat(q)
        if chat_response is None:
            try:
                context_query = f"{q}, if this query needs internet research, respond with 'internet' only, ***Reply like Tony Stark's Jarvis in fewer words. If it's to perform an action on the computer, write complete code in Python, nothing else.***"
                rep = cached_function(context_query, ChatGpt, context_query)
                try:
                    code = filter(rep)
                    if code:
                        success, error = execute_code_with_cache(code)
                        if success:
                            execute_code_with_cache(ChatGpt(f"Output: {success}, respond for this action if it is, or else ask for any another help"))
                        else:
                            off(f"Error executing code: {error}")
                    else:
                        on(rep)
                except Exception as e:
                    print(e)
            except Exception as e:
                off(locallm(q))
        else:
            off(chat_response)

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.Intro()

    def Intro(self):
        ChatGpt(get_extension_info())
        ChatGpt(f"user is using {get_os_info()}")
        off(ChatGpt("greet user in your style that is jarvis style note this is a system prompt"))
        while True:
            q = Listen()
            if q:
                process_voice_input(q)

startExecution = MainThread()
startExecution.start()
'''
class Main(QMainWindow):
    cpath = ""

    def __init__(self, path):
        self.cpath = path
        super().__init__()
        self.ui = Ui_JarvisUI(path=current_path)
        self.ui.setupUi(self)
        self.ui.pushButton_4.clicked.connect(self.startTask)
        self.ui.pushButton_3.clicked.connect(self.exitTask)

    def startTask(self):
        startExecution.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/ironman1.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/ringJar.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/circle.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/lines1.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/ironman3.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/circle.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/powersource.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/powersource.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/ironman3_flipped.gif")
        self.ui.label_16.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}/UI/Sujith.gif")
        self.ui.label_17.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    def exitTask(self):
        exitTask()
        sys.exit()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

current_path = os.getcwd()
app = QApplication(sys.argv)
jarvis = Main(path=current_path)
jarvis.show()
exit(app.exec_())
'''

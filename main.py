import os
import sys
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow
from JarvisUi import Ui_JarvisUI
from func.basic.listenpy import Listen
from func.basic.chat import chat
from llm.chatgpt import ChatGpt
from llm.filter import filter
from llm.bard import response
from func.OF.dataonline import online_scraper
from func.OF.youtube import get_transcript, transcription
from func.Powerpointer.main import generate_powerpoint
from func.ocr.ocroff import ocr_off
from func.ocr.ocron import ocr_on
from func.speak.speakmid import mid as off
from func.speak.speakon import speak as on
from func.OF.youtube import get_transcript, transcription
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
import requests

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
    os_name = platform.system()
    if os_name == 'Linux':
        dist_name, version, codename = platform.linux_distribution()
        return f"Operating System: {os_name}\nDistribution: {dist_name}\nVersion: {version}\nCodename: {codename}"
    else:
        return f"Operating System: {os_name}"

def get_extension_info():
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
    
    return extensions_info


def exitTask():
    subprocess.Popen(["python", "app.py"])

def cookie_bing():
    try:
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            bing = config.get('cookie_bing')
            if bing is None:
                raise ValueError("cookie_bing not found in config file")
            return bing
    except FileNotFoundError:
        print("Config file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON in config file.")
    except Exception as e:
        print(f"Error reading config file: {e}")


def generate_images(prompt):
    # Enclose the prompt within quotes
    command = f"python -m BingImageCreator -U {cookie_bing()} --prompt \"{prompt}\""
    system(command)
    files = listdir("output")
    # Reverse the list of files and select the last four elements
    return files[-4:]


def play_youtube_video(video_query):
    try:
        kit.playonyt(video_query)
    except Exception as e:
        print("An error occurred:", str(e))


def url():
    try:
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            url = config.get('URL')
            if url is None:
                raise ValueError("URL not found in config file")
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


def process_voice_input(q):
    if any(keyword in q for keyword in ["bye", "see you later", "terminate"]):
        on("Bye sir, have a great day")
        exitTask()
        sys.exit()

    elif any(keyword in q for keyword in ["learn", "research"]):
        server_thread = threading.Thread(target=start_server, args=("127.0.0.1", "12345"))
        server_thread.start()
        q = q.lower.replace("research", "")
        q = q.lower.replace("learn", "")
        q = q.lower.replace("about", "")
        start_work(q)

    elif any(keyword in q for keyword in ["translate", "summarize", "transcribe"]):
        on("Please wait..")
        video_id = get_transcript()
        summary = transcription(video_id)
        off(ChatGpt(f"Summarize this transcription in points: {summary}"))

    elif any(keyword in q for keyword in ["powerpoint", "presentation"]):
        q = q.replace("create", "")
        q = q.replace("a", "")
        q = q.replace("powerpoint", "")
        q = q.replace("presentation", "")
        q = q.replace("on", "")
        q = q.replace("Create", "")
        os.startfile(generate_powerpoint(q))

    elif any(keyword in q for keyword in ["study", "this", "text", "code"]):
        keyboard.press_and_release("ctrl + c")
        clipboard = pyperclip.paste()
        rep = ChatGpt(q + clipboard + "if it needs to write on file use python code that tooo full code, do not write anything except code")
        code = filter(rep)
        if code:
            success, error = execute_code(code)
            if success:
                on(ChatGpt(f"You successfully completed the task for {q}. Respond for your successful completion."))
            else:
                off(f"Error executing code: {error}")
        else:
            off(rep)
    
    elif any(keyword in q for keyword in ["Jarvis", "jarvis"]):
        code = ChatGpt(q + " ***Use Python programming language. Just write complete code nothing else***")
        code = filter(code) if code else None
        if code:
            success, error = execute_code(code)
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
            ocr_on(q,url=url(), double_click=double_click)
        except:
            ocr_off(q, double_click=double_click)

    else:
        if chat(q) is None:
            try:
                a = online_scraper(q)
                rep = ChatGpt(f"{q}, if this query needs internet research, this is your context: {a}. ***Reply like Tony Stark's Jarvis in fewer words. If it's to perform an action on the computer, write complete code in Python, nothing else.***")
                code = filter(rep)
                if code:
                    success, error = execute_code(code)
                    if success:
                        on(ChatGpt(f"You successfully completed the task for {q}. Respond for your successful completion."))
                    else:
                        off(f"Error executing code: {error}")
                else:
                    off(rep)
            except Exception as e:
                off(f"Error occurred: {e}")
        else:
            on(chat(q))

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
    
    def run(self):
        self.Intro()
        
    def Intro(self):
        ChatGpt(get_extension_info())
        ChatGpt(f"user is using {get_os_info()}")
        while True:
            q = Listen()
            if q:
                process_voice_input(q)

startExecution = MainThread()

class Main(QMainWindow):
    cpath =""
    
    def __init__(self,path):
        self.cpath = path
        super().__init__()
        self.ui = Ui_JarvisUI(path=current_path)
        self.ui.setupUi(self)
        self.ui.pushButton_4.clicked.connect(self.startTask)
        self.ui.pushButton_3.clicked.connect(self.exitTask)
    
    def startTask(self):
        startExecution.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman1.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ringJar.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\circle.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\lines1.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman3.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\circle.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\powersource.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\powersource.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman3_flipped.gif")
        self.ui.label_16.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\Sujith.gif")
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


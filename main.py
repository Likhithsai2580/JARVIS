import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import pyjokes #pip install pyjokes

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    
    speak("loading jarvis")
    speak("getting database")
    speak("Loading Database")
    speak("turning servers all on")
    speak("connecting to satellite number thirty five")
    speak("connected successfully")
    speak("connecting to online")
    speak("success now in i am at online")
    speak("booting jarvis ")
    speak("booted jarvis successfully")
    speak("connecting jarvis to you")
    speak("connected successfully")
    speak("turning on graphical user interface")
    rainmeter = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Rainmeter.lnk"
    os.startfile(rainmeter)
    speak("success i am at graphical mode")
    speak("I am Jarvis Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"Sir said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'what is' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print("According to Wikipedia")
            print(results)
            speak(results)

        if 'who is' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print("According to Wikipedia")
            print(results)
            speak(results)

        if 'how' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print("According to Wikipedia")
            print(results)
            speak(results)

        if 'explain' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print("According to Wikipedia")
            print(results)
            speak(results)
        
        if 'tell me a joke' in query:
            speak("here we go ")
            speak(pyjokes.get_joke())
            print(pyjokes.get_joke())

        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("opening gooogle")
            webbrowser.open("google.com")

        elif 'open my youtube channel' in query:
            speak("opening youtube channel hackers are here where are you")
            webbrowser.open("https://www.youtube.com/channel/UC5N_8t5SzEyJrTx1bC66Kpw")
        
        elif 'open scratch' in query:
            speak("opening scratch")
            scratch = "C:\\Program Files\\Scratch Desktop\\Scratch Desktop.exe"
            os.startfile(scratch)

        if 'how are you' in query:
            speak("thank you for asking i am great")
            speak("how are you")

        if 'i am fine' in query:
            speak("great")

        elif 'shutdown the laptop' in query:
            speak("bye sir")
            speak("shuting down pc ")
            os.system('shutdown -s -t')

        elif 'restart the laptop' in query:
            speak("restarting pc")
            os.system('shutdown -r -t')
 

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "D:\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'who made you' in query:
            speak("S LIKHITH SAI made me and named as jarvis")
        
        elif 'bye' in query:
            speak("bye sir exiting from code written by lucky")
            exit()

        elif 'open my website' in query:
            speak ("opening website")
            webbrowser.open("https://www.sites.google.com/veiw/hackersareherewhereareyou")

        elif 'email ' in query:
            try:
                speak("to whom")
                emailto = input("please input email")
                speak("What should I say?")
                content = takeCommand()
                to = emailto   
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my sir. I am not able to send this email")    
        elif 'my name is' in query:

            speak("what is your name  write here")
            name = input("mention here!!!!!!!!!!!")
        elif 'what is my name' in query:
            speak("your name is", name)
        elif 'hey jarvis' in query:
            speak("sir i am Listening")
        elif 'how may I help you' in query:
            speak("sir you can help me by saying me")

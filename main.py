import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib

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
    speak("turning servers all on")
    speak("connecting to online")
    speak("success now in am at online")
    speak("booting jarvis ")
    speak("booted jarvis successfull")
    speak("connecting jarvis to you")
    speak("connected successfully")
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
        print(f"User said: {query}\n")

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
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("oping gooogle")
            webbrowser.open("google.com")

        elif 'open my youtube channel' in query:
            speak("opening youtube channel hackers are here where arre you")
            webbrowser.open("https://www.youtube.com/channel/UC5N_8t5SzEyJrTx1bC66Kpw")
        
        elif 'open scratch' in query:
            speak("opening scratch")
            scratch = "C:\\Program Files\\Scratch Desktop\\Scratch Desktop.exe"
            os.startfile(scratch)

        elif 'shutdown the laptop' in query:
            speak("bye sir")
            speak("shuting down pc ")
            os.system('shutdown -s')

        elif 'restart the laptop' in query:
            speak("restarting pc")
            os.system('shutdown -r')
 

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
                speak("Sorry my friend sir. I am not able to send this email")    
        

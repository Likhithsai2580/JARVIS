import speech_recognition as sr
import colorama
from colorama import Fore, Style

def Listen():
    colorama.init(autoreset=True)
    
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 200  
    recognizer.pause_threshold = 0.5  
    recognizer.operation_timeout = None  
    
    with sr.Microphone() as source:
        print(Fore.YELLOW + Style.BRIGHT + "Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio_data = recognizer.listen(source, timeout=5)  # Set timeout here
            print(Fore.GREEN + Style.BRIGHT + "Recognizing...")
            text = recognizer.recognize_google(audio_data)
            
            print(Fore.GREEN + Style.BRIGHT + f"User: {text}")
            return text
        
        except sr.WaitTimeoutError:
            print(Fore.RED + Style.BRIGHT + "Timeout: No speech detected. Please speak louder or check your microphone.")
            return None
        
        except sr.UnknownValueError:
            print(Fore.RED + Style.BRIGHT + "Failed to recognize audio. Please try again.")
            return None
        
        except sr.RequestError as e:
            print(Fore.RED + Style.BRIGHT + f"Speech recognition request failed: {e}. Please check your internet connection.")
            return None
        
        except TimeoutError:
            print(Fore.RED + Style.BRIGHT + "Operation timed out. Please try again.")
            return None

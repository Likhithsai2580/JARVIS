import pyttsx3
import colorama
from colorama import Fore, Style
import os
from functools import lru_cache

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Cache the 'off' function
@lru_cache(maxsize=128)  # Adjust maxsize according to your memory constraints
def off(text):
    colorama.init(autoreset=True)
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"J.A.R.V.I.S : {text}")
    # Save text to MP3 file
    engine.say(text)
    engine.runAndWait()

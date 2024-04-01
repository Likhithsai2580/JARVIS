import pyttsx3
import colorama
from colorama import Fore, Style
import os

engine = pyttsx3.init()

# Check all available voices
voices = engine.getProperty('voices')
engine.setProperty('rate', 200)
# Set Microsoft David voice if available
for voice in voices:
    if "microsoft david desktop - english (united states)" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def off(text):
    colorama.init(autoreset=True)
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"J.A.R.V.I.S : {text}")
    # Save text to MP3 file
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    off("Testing off function")  # For testing

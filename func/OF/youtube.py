from functools import lru_cache
from time import sleep
from keyboard import press_and_release
import pyperclip
from youtube_transcript_api import YouTubeTranscriptApi

# Cache the 'get_transcript' function
@lru_cache(maxsize=128)  # Adjust maxsize according to your memory constraints
def get_transcript_cached():
    clip = ""
    for i in range(5):
        press_and_release("ctrl + l")
        sleep(1)
        press_and_release("ctrl + c")
        clip = pyperclip.paste()
        if "https://www.youtube.com/watch?" in clip:
            break
        else:
            sleep(1)
    
    if "v=" in clip:
        url = clip.split("v=")[1].split("&")[0]
        return url
    else:
        return "URL not found in clipboard content"

# Cache the 'transcription' function
@lru_cache(maxsize=128)  # Adjust maxsize according to your memory constraints
def transcription_cached(video):
    try:
        return str(YouTubeTranscriptApi.get_transcript(video))
    except:
        return None

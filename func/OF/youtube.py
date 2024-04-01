from time import sleep
from keyboard import press_and_release
import pyperclip
from youtube_transcript_api import YouTubeTranscriptApi
def get_transcript():
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

def transcription(video):
    try:
        return str(YouTubeTranscriptApi.get_transcript(video))
    except:
        return None


import pywhatkit as kit

def play_youtube_video(video_query):
    try:
        kit.playonyt(video_query)
    except Exception as e:
        print("An error occurred:", str(e))


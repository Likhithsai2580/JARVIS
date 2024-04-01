import sounddevice as sd
import numpy as np

threshold = 43

def detect_clap(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > threshold:
        print("Clap detected!")
        return True
    return False

def listen_for_claps():
    with sd.InputStream(callback=detect_clap):
        sd.sleep(1000)

def main_clap_exe():
    print("waiting for clap")
    while True:
        if listen_for_claps():
            return True

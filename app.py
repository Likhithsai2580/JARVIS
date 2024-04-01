from func.basic.listenpy import Listen
import os

while True:
    q = Listen()
    if q and ("jarvis" in q.lower()):
        os.startfile("main.py")
        break  # Exit the loop after executing the action

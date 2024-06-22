from func.OF.obj_detect import *
from llm.chatgpt import ChatGpt
from llm.filter import filter
from func.basic.listenpy import Listen
cache = {}
CACHE_EXPIRATION_TIME = 3600

def execute_code(code):
    try:
        exec(code)
        return True, None
    except Exception as e:
        return False, e

def cached_function(key, func, *args, **kwargs):
    # Check if the result is cached and not expired
    if key in cache and cache[key]['expiration'] > time.time():
        return cache[key]['result']
    # Call the function and cache the result
    result = func(*args, **kwargs)
    cache[key] = {'result': result, 'expiration': time.time() + CACHE_EXPIRATION_TIME}
    return result

def execute_code_with_cache(code):
    # Cache the execution result based on code
    return cached_function(code, execute_code, code)

def Eye(q):
    while True:
        img_discription=capture_and_send_image()
        context_query = f"{q}, if this query needs internet research, respond with 'internet' only, ***Reply like Tony Stark's Jarvis in fewer words. If it's to perform an action on the computer, write complete code in Python, nothing else.***, LIVE CAM is ON {img_discription} (to close webcam reply only stop and nothing else)"
        rep = cached_function(context_query, ChatGpt, context_query)
        if "STOP" in rep.capitalize:
            break
        else:
            try:
                code = filter(rep)
                success, error = execute_code_with_cache(code)
                if success:
                    execute_code_with_cache(ChatGpt(f"Output: {success}, respond for this action if it is, or else ask for any another help"))
                else:
                    execute_code_with_cache(ChatGpt(f"{error}"))
            except Exception as E:
                print(f"Falied {E}")

def EYE():
    resp = Listen()
    Eye(resp)

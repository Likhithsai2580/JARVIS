from jinja2 import Template
import os
from pathlib import Path
import datetime
import platform
from functools import cache
from dotenv import get_key

PROMPTS_DIR = fr"{os.path.join(os.getcwd(), 'func', 'rawdog', 'prompts')}"


def listdir():
    cwd = Path.cwd()

    entries = list(cwd.iterdir())

    file_details = []
    dir_details = []

    for entry in entries:
        modified_time = datetime.datetime.fromtimestamp(entry.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        size = entry.stat().st_size
        
        if entry.is_file():
            type_str = 'bytes'
            name = entry.name
            file_details.append((modified_time, size, type_str, name))
        elif entry.is_dir():
            type_str = 'items'
            name = '/' + entry.name  # prepend '/' to directory names
            dir_details.append((modified_time, size, type_str, name))
        else:
            type_str = ''
            name = entry.name
        
    file_details.sort(key=lambda x: x[3])

    dir_details.sort(key=lambda x: x[3])

    sorted_details = file_details + dir_details

    to_return = ""
    
    for detail in sorted_details:
        formatted_line = f"{detail[0]:19} {detail[1]:10} {detail[2]:6} {detail[3]}"
        to_return +=str(formatted_line)+"\n"
    return to_return[:-1]

@cache
def whichOs():
    return platform.system()

@cache
def rawdogPrompt():
    with open(os.path.join(PROMPTS_DIR, "rawdog.jinja2"), "r") as f:
        return f.read()

@cache
def examplePrompt():
    with open(os.path.join(PROMPTS_DIR, "example.jinja2"), "r") as f:
        return f.read()


def startinfoPrompt():
    with open(os.path.join(PROMPTS_DIR, "startinfo.jinja2"), "r") as f:
        string = f.read()
        
    data = {
    'date': datetime.datetime.now().strftime('%Y-%m-%d'),
    'time': datetime.datetime.now().strftime('%H:%M:%S'),
    'cwd': os.getcwd(),
    'os': whichOs(),
    'listdir': listdir(),
    }
    template = Template(string)
    rendered_output = template.render(data)
    return rendered_output


def Prompts():
    return [
        {
        "role": "system",
        "content": rawdogPrompt()
        },
        {
        "role": "system",
        "content": examplePrompt()
        },
        {
        "role": "system",
        "content": startinfoPrompt()
        }
    ]

if __name__ == "__main__":
    from rich import print
    print(startinfoPrompt())


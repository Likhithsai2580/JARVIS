import json
import os

PROMPTS_DIR = fr"{os.path.join(os.getcwd(), 'plugins', 'codebrew', 'prompts')}"
SAMPLES_DIR = fr"{os.path.join(os.getcwd(), 'plugins', 'codebrew', 'json')}"

def codebrewPrompt():
    with open(os.path.join(PROMPTS_DIR, "codebrew.jinja2"), "r") as f:
        return f.read()

def samplePrompt():
    with open(os.path.join(SAMPLES_DIR, "example.json"), "r") as f:
        _json = json.loads(f.read())[:2]
        to_return = []
        for item in _json:
            to_return += item["response"]
        return to_return

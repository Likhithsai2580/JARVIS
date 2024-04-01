import random
import json
import torch

from data.chatbot.model import NeuralNet
from data.chatbot.nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data/chatbot/intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data/chatbot/data.pth"
data = torch.load(FILE, map_location=torch.device('cpu'))

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "J.A.R.V.I.S"
def chat(prompt):
    sentence = prompt
    if sentence == "quit":
        exit()

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.999999999999999999:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return str(f"{random.choice(intent['responses'])}")
    else:
        return None

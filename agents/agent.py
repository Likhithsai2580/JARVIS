from agents.llm_for_agent import ChatGpt, response, mistral_7b
import socket

def send_message(host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(message.encode())
    data = client_socket.recv(1024)
    print("Received:", data.decode())
    client_socket.close()


HOST = '127.0.0.1'
PORT = 12345

def question_framer(topic):
    questions = ChatGpt(f"Consider the topic of {topic}. What aspect of this topic am I curious about or seeking clarity on? What specific question can I formulate that will help me delve deeper into understanding this aspect? Give me only questions about to think about")
    return questions

def start_work(topic):
    resp = response(question_framer(topic))
    summary = mistral_7b(f"summarize this {resp}")
    send_message(HOST, PORT, summary)

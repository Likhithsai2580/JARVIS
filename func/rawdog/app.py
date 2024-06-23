from llm.chatgpt import ChatGpt
from func.rawdog import RawDog

def main():
    # Instantiate LLM
    llm_instance = ChatGpt()

    # Instantiate RawDog with a prompt and the LLM instance
    prompt = "Enter your prompt here:"
    raw_dog_instance = RawDog(prompt, llm_instance)

    # Example usage
    raw_dog_instance.run()

    # After running, you can access messages stored in llm_instance.messages
    for message in llm_instance.messages:
        print(f"{message['role']}: {message['content']}")

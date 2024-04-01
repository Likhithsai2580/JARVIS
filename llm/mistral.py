from gradio_client import Client

client = Client("https://osanseviero-mistral-super-fast.hf.space/")

def mistral_7b(user_input):

    result = client.predict(
        user_input,
        0.6,
        1024,
        0.9,
        1.1,
        api_name="/chat"
    )
    return result
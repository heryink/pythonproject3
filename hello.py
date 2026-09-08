from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = Anthropic(api_key=api_key,base_url="https://openrouter.ai/api")

def add_user_message(messages,user_input):
    messages.append({"role":"user","content":user_input})

def add_assistant_message(messages,response):
    messages.append({"role":"assistant","content":response})

model="Anthropic/claude-sonnet-4-5"
def chat(messages,system=None,temperature=None):
    params = {
        "model":model,
        "max_tokens":96,
        "messages":messages}

    if system:
        params['system'] = system
    if temperature:
        params['temperature'] = temperature

    with client.messages.stream(**params) as response:
        for text in response.text_stream:
            print(text,end="",flush=True)
        final_message = response.get_final_message()
        return final_message.content[0].text



    return response.content[0].text
messages = []

while True:
    try:
        user_input = input(">>> ")
        add_user_message(messages, user_input)
        response = chat(messages, temperature=1)
        print()
        add_assistant_message(messages, response)
    except Exception as e:
        print(f"error occurred{e}")



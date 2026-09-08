from anthropic import Anthropic
import os
from dotenv import load_dotenv
from tool import scrape_web, scrape_web_schema

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = Anthropic(
    api_key=api_key,
    base_url="https://openrouter.ai/api")

model = "anthropic/claude-sonnet-4-5"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    response = client.messages.create(
        model=model,
        max_tokens= 1000,
        messages=messages,
        tools=[scrape_web_schema])
    # Claude wants to use a tool

    if response.stop_reason == "tool_use":
        print(response)
        tool_use_block = response.ToolUseBlock  #next(block for block in response.content if block.type == "tool_use") #returns the first item in an iterable that satisfies the condition
        tool_name = tool_use_block.name
        tool_input = tool_use_block.input

        if tool_name == "scrape_web":
            result = scrape_web(tool_input["url"])
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use_block.id,
            "content": result
        }]})
        final_response = client.messages.create(
            model=model,
            max_tokens=1000,
            messages=messages,
            tools=[scrape_web_schema]
        )
        return final_response.content[0].text

    return response.content[0].text


messages = []

while True:
    user_input = input(">>> ")
    if user_input.lower() == "quit":
        break
    add_user_message(messages, user_input)
    response = chat(messages)
    add_assistant_message(messages, response)
    print(response)



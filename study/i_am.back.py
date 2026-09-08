import anthropic
from pydantic import BaseModel,Field
import json

def add_user_message(message,user_input):
    message.append({"role":"user","content":user_input})

def add_assistant_answer(message, output):
    message.append({"role":"user","content":output})


def chat(chats):
    client = anthropic.Anthropic(base_url=,api_key=)
    result = client.messages.create(
    model="haiku-4-5",
    max_tokens=1000,
    temperature=0.6,
    messages=[{"role":"user","content":chats}]
)
    return result.content[0].text


class CustomerInfo(BaseModel):
    name: str = Field(description="name of the customer")
    age: int = Field(description="age of the customer")
    location: str =Field(description="where the customer lives")

json_schema = CustomerInfo.model_json_schema()

print(json.dumps(json_schema, indent=2))

message=[]
while True:
    user_input=input(">>> ")
    add_user_message(message)
    output=chat(message)
    add_assistant_answer(output)



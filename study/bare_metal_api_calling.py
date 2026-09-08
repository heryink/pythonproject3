import requests
import json

url ="https://openrouter.ai/api/v1/chat/completions"

headers = {"Authorization": "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",
           "content-type": "application/json"
           }
payload = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello!"}
    ]
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()

print(data)


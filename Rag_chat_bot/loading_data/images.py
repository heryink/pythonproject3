from pathlib import Path
import base64
from openai import OpenAI

img_path = Path(r"C:\Users\USER\PycharmProjects\PythonProject3\imagee.jpg")

client = OpenAI(base_url=, api_key=)

with open(img_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    prompt = ("Extract the text from the image attached. Make sure to only "
    "extract only the text. If there is no text in the image, "
    "please return with the sentence 'No text found in the image." )

    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[{"role": "user",
                   "content": [
                       {"type": "text","text": "prompt"},
                       {"type": "image", "image": f"{base64_image}"}
                   ]
                }],
        max_tokens=500)

    content = response.choices[0].message.content
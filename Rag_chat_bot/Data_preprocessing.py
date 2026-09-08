#Storing metadata alongside chunks
import PyPDF2
import os
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

file_path = r"C:\Users\USER\PycharmProjects\PythonProject3\Rag_chat_bot\Rag_chat_bot\pdf_files\attention_is_all_you_need_paper.pdf"

with open(file_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    metadata = dict(reader.metadata)
    print(metadata)

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    metadata["page_count"] = len(reader.pages)
    metadata["file_path"] = file_path
    metadata["file_name"] = os.path.basename(file_path)
    metadata["text_length"] = len(text)
    metadata["file_size"] = os.path.getsize(file_path)
    print(metadata)

load_dotenv()
client = OpenAI(api_key=os.getenv("openrouter_api_key"), base_url="https://openrouter.ai/api/v1")

class AuthorContact(BaseModel):
    name:str
    email:str
    company:list[str]

class Contacts(BaseModel):
    entries: list[AuthorContact]

system_message = """Extract the contact information of all authors."""

response = client.beta.chat.completions.parse(
    model="openai/gpt-4o-mini",
    messages=[{
        "role": "system", "content":system_message },{
        "role":"user", "content":text}],
    response_format=Contacts)

author_contacts = response.choices[0].parsed
metadata_ext_llm = metadata
metadata_ext_llm["author_contacts"] = author_contacts




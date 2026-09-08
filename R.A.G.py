#CHUNK BY CHARACTER,
from dotenv import load_dotenv
import voyageai

def chunk_by_text(text,chunk_side=170, chunk_overlap = 20):
    chunks = []
    start_idx = 0

    while start_idx < len(text):
        end_idx = min(start_idx + chunk_overlap,text)

        chunk_text = text[start_idx:end_idx]
        chunks.append(chunk_text)
        start_idx = end_idx - chunk_overlap
    return chunks

#chunk by sentence or sections
import re

def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    start_idx = 0

    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        current_chunk = sentences[start_idx:end_idx]
        chunks.append(" ".join(current_chunk))

        start_idx += max_sentences_per_chunk - overlap_sentences

        if start_idx < 0:
            start_idx = 0
    return chunks



def chunk_by_sections(document_text):
    """"if it is seperated by markdowns or structure is known and consistent"""
    pattern = r"\n## "
    return re.split(pattern, document_text)

with open("./report.md","r") as f:
    text = f.read()

chunks = chunk_by_sections(text)
load_dotenv()
client = voyageai.Client()

# using the embedding model to generate vectors for the chunks using vogage ai through api
def generate_embedding(text_chunk, model="voyage-3-large",input_type="query"):
    input = text_chunk if isinstance(text_chunk, list) else [text_chunk]
    result = client.embed(input,model=model,input_type=input_type)
    return result.embeddings if isinstance(text_chunk, list) else result.embeddings[0]


embeddings = generate_embedding(chunks)

#vector database to store and add each embedding

store = Vectorindex()

for embedding, chunk in zip(embeddings,chunks):
    store.add_vector(embedding, {"content": chunk})

user_embedding = generate_embedding("what did software engineers do last week")

result = store.search(user_embedding,2)

for doc, distance in result:
    print(distance)
    print(doc[0:200 ])




mport numpy as np
import pandas as pd
import chromadb
from cohere import ClientV2
import os
from dotenv import load_dotenv


# Load the metadata
df = pd.read_csv('arxiv_papers_5k.csv')
dataset = pd.DataFrame(df)
print(f"Loaded {len(df)} papers")

#load embeddings of files
embeddings = np.load("embeddings_cohere_5k.npy")
print(f"Loaded embeddings {embeddings.shape}")
print(len(embeddings[0]))

assert len(df) == len(embeddings)
#Creating collections
client = chromadb.Client()

collection = client.create_collection(
    name="arxiv_science_papers",
    metadata={"description": "5000 arXiv papers from computer science"})

ids = [f"paper{i}" for i in range(len(df))]

data = df.iterrows()

print(next(data))
print(next(data))

metadata = [{
        "title": row["title"],
        "category": row["category"],
        "authors": row["authors"],
        "year": row["published"]}   for _, row in df.iterrows()]


documents = df['abstract'].to_list()

batch_size = 400
for x in range(0, len(embeddings), batch_size):
    batch_end = min(x+batch_size, len(embeddings))
    print(f"  Batch {x // batch_size + 1}: Adding papers {x} to {batch_end}")

    collection.add(
        ids=ids[x:batch_end],
        embeddings=embeddings[x:batch_end].tolist(),
        metadatas=metadata[x:batch_end],
        documents=documents[x:batch_end])


#Retriving
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("Api key not found!!!")


client_e = ClientV2(api_key=api_key)
print("api key loaded")

question = "what is an autoregressive model?"
response = client_e.embed(model="embed-v4.0", input_type="search_query", texts=[question],  embedding_types=["float"])
question_embeddings = response.embeddings.float[0]

results = collection.query(query_embeddings=question_embeddings, n_results=5)


for i in range(len(results['ids'][0])):
    paper_id = results['ids'][0][i]
    distance = results['distances'][0][i]
    metadata = results["metadatas"][0][i]

    print(f"\n{i + 1}. {metadata['title']}")
    print(f"   Category: {metadata['category']} | Year: {metadata['year']}")
    print(f"   Distance: {distance:.4f}")
    print(f"   Abstract: {results['documents'][0][i][:150]}...")





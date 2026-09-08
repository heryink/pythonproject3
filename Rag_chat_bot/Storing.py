from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


def chunk_text(text, chunk_size=100, overlap=20):
    chunks, start_idx = [], 0
    end_idx = start_idx + chunk_size

    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))
        if end_idx < len(text):
            bp = text.rfind("\n\n", start_idx, end_idx)
            if bp == -1:  # if not found
                text.rfind(". ", start_idx, end_idx)
            if bp > start_idx:
                end_indx = bp + 1

            chunk = text[start_idx:end_idx].strip()
            if chunk:
                chunks.append(chunk)
            start_idx = end_idx - overlap if end_idx < len(text) else end_idx
    return chunks


file_path = Path(r"C:\users\user\Downloads\subtitle.txt")
text = file_path.read_text(encoding="utf-8")
chunks = chunk_text(text)
print(chunks)

## Embed and store in ChromaDb
client = Sentence


def embed_and_store(chunks, db_path, collection_name):
    chroma = chromadb.PersistentClient(path=str(db_path))
    collection = chroma.get_or_create_collection(
        name=collection_name,
        metadata={"description": "Business analysis course subtitle"}
    )

    embeddings = []
    for i in range(0, len(chunks), 100):
        batch = chunks[i: i + 100]
        res = client.embeddings.create(model=embedding_model, input=batch)
        embeddings.extend([x.embedding for x in res.data])

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"chunk_index": i} for i in range(len(chunks))]
    )
    return collection


chroma_db_dir = Path("chroma_db")
collection = embed_and_store(chunks, chroma_db_dir, "subtitle.txt")


##Tesy retrieval

def retrieve(query, top_k=3):
    q_emb = client.embeddings.create(
        model=embedding_model,
        input=query
    ).data[0].embedding

    res = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents"],
    )

    return res["documents"][0]


question = "what are the roles of business analyst"
docs = retrieve(question)


##text generation

def answer(question, docs):
    context = "\n\n --\n\n".join(docs)
    prompt = f"""Answer the question using only the context
    Context:
    {context}

    Question:
    {question}

    Answer:"""

    res = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}])
    return res.choices[0].message.content


question = "what are the the day to day activites of business analyst"
docss = retrieve(question)
answer_text = answer(question, docss)










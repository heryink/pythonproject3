from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier

pdf_files = [{
    "file_path": r"C:\Users\USER\PycharmProjects\PythonProject3\Rag_chat_bot\Rag_chat_bot\pdf_files\attention_is_all_you_need_paper.pdf",
    "name": "attention is all you need"},
    {"file_path":r"C:\Users\USER\PycharmProjects\PythonProject3\Rag_chat_bot\Rag_chat_bot\pdf_files\premier_league_history.pdf",
     "name":"premier league history"},
    {"file_path":r"C:\Users\USER\PycharmProjects\PythonProject3\Rag_chat_bot\Rag_chat_bot\pdf_files\AI_in_Factories_Discussion_Cleaned.pdf",
    "name":"AI_in_Factories"}]

chunks_dict_list = []
#read files
for file in pdf_files:
    with open(file["file_path"], "rb") as f:
        reader =  PyPDF2.PdfReader(f)

        text = ""
        for page in reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200,
                                                       chunk_overlap=20,
                                                       is_separator_regex=False)
        chunks = text_splitter.split_text(text)

        for chunk in chunks:
            chunks_dict_list.append({"text":chunk,
                                     "name": file["name"]})

chunks_df = pd.DataFrame(chunks_dict_list)
print(chunks_df.tail())

model_path = r"C:\Users\USER\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
model =   SentenceTransformer(model_name_or_path=model_path)

embeddings = []

for text in chunks_df["text"]:
    embeddings.append(model.encode(text))
assert len(embeddings) == len(chunks_df["text"])
chunks_df["embeddings"] = embeddings

print(chunks_df.columns)

y = chunks_df['name']
X = chunks_df['embeddings'].apply(
    lambda x: pd.Series(eval(x) if isinstance(x, str) else pd.Series(x))
)# pd.series creates multiple columns for the embeddings just like one hot encoder
 #eval(X) parses if it is a string

classifier = RandomForestClassifier()
classifier.fit(X,y)

question = "tell me about ai companies?"
question_embedding = model.encode(question)

X_test = [question_embedding]

predicted_class = classifier.predict(X_test)
print(predicted_class)
probabilities = classifier.predict_proba(X_test)
print(probabilities)

from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import os

texts = ["coding is actually kinda fun when the code works",
        "n8n is slowly becoming my favorite rabbit hole",
        "i think automation is pretty cool",
        "my code worked and i honestly don't know why",
        "debugging for three hours just to find a missing comma",
        "i came to write one line of code and somehow built a whole project",
        "learning python is fun until python decides otherwise",
        "these vectors are starting to look less like random numbers",
        "i put my sentences into a model and now they have coordinates",
        "my sentences are literally hanging out in vector space"]

os.environ["HF_HUB_OFFLINE"] = "1"

model_path = r"C:\Users\USER\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
embed = SentenceTransformer(model_name_or_path=model_path)
embeddings = []
print(embeddings)

for text in texts:
    embeddings.append(embed.encode(text))

embeddings_df = pd.DataFrame(embeddings, columns=[f"dim_{i}" for i in range(len(embeddings[0]))])
pca = PCA(n_components=2)
embeddings_df_reduced = pca.fit_transform(embeddings_df)
embeddings_df_reduced = pd.DataFrame(embeddings_df_reduced, columns=["PC1","PC2"])
embeddings_df_reduced['texts'] = texts
print(embeddings_df_reduced)

plt.scatter(embeddings_df_reduced["PC1"], embeddings_df_reduced["PC2"])


#add labels to each plot
for i, labels in enumerate(embeddings_df_reduced["texts"]):
    plt.text(embeddings_df_reduced['PC1'][i], embeddings_df_reduced['PC2'][i], labels, fontsize=9)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Scatter Plot")
plt.show()

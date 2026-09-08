import numpy as np
from sentence_transformers import SentenceTransformer



class Vector_DB:
    def __init__(self):
        self.vectors = []    #store embeddings in an array

    # add vector to database(array)
    def add_vector(self, vect_id, vector, metadata=None):
        record = {
            "vect_id": vect_id,
            "vector": np.array(vector, dtype=np.float32),
            "metadata": metadata
        }
        self.vectors.append(record)

    #Retrieve all vector from database
    def get_all_vectors(self):
        return self.vectors

    def _cosine_similarity(self, vect_a, vect_b):
        #calculate dot product
        dot_prd = np.dot(vect_a, vect_b)

        mag_a = np.linalg.norm(vect_a) #magnitude of vector a
        mag_b = np.linalg.norm(vect_b) #magnitude of vector b

        #cosine similarity
        cos_sim = dot_prd / (mag_b * mag_a + 1e-8) # small epsilon to avoid division by zero

        return cos_sim

    #search for similarity vectors and return top_k result
    def search(self, query_vector, top_k=3):
        query_vector = np.array(query_vector, dtype=np.float32)

        result = [] # Stores the top_k results


        for record in self.vectors:
            sim = self._cosine_similarity(query_vector, record["vector"])

            result.append({
                "vect_id": record["vect_id"],
                "similarity": sim,
                "metadata":record["metadata"]
            })

            result.sort(key= lambda x: x["similarity"], reverse=True)

        return result[:top_k]



#Testing

db = Vector_DB()

db.add_vector("vec_1", np.random.rand(5), "first vector")
db.add_vector("vect_2", np.random.rand(5), metadata=" second vector")
db.add_vector("vect_2", np.random.rand(5), metadata=" third vector")
db.add_vector("vect_3", np.random.rand(5), metadata=" fourth vector")
db.add_vector("vect_3", np.random.rand(5), metadata=" fifth vector")



query_vector = np.random.rand(5)

output = db.search(query_vector=query_vector,top_k=3)
for result in output:
    print(f"ID: {result["vect_id"]}| similarity:{result["similarity"]:.3f}| metadata: {result["metadata"]}")


embedding_model = "text-embedding-3-small"
model = SentenceTransformer(model_name_or_path="all-MiniLM-L6-v2")


sentences = [" i love hod vector databases word",
             "rag isnt that bad afterall",
             "i need to install sentence transformaer with school wifi first thing when i get to school",
             "learning math is not bad afterall",
             "set notations is quite nice if you can interpret them"]

new_db = Vector_DB()

for idx, sentence in enumerate(sentences):
    #create sentence embeddings
    vector = model.encode(sentence)

    new_db.add_vector(vect_id=f"sent_{idx}", vector=vector, metadata={f"sentence": sentence}) #add sentence embedding to vector database

#query database

question = "i would love to know how to read math"
query_vector = model.encode(question)
result = new_db.search(query_vector)
print(query_vector)

print(question)
for res in result:
    print(f"Similar Sentence: {res['metadata']['sentence']}")
    print(f"Cosine Similarity Score: {res['similarity']:.2f}\n")





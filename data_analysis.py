import numpy as np

data = ["the cat sits", "cat sleeps on mat", "dog runs fast"]
vocab = set(" ".join(data).split())
print(vocab)



np.random.seed(42)
import numpy as np

def cosine_similarity(vecA, vecB):
    vectorA = np.array(vecA['embedding'])
    vectorB = np.array(vecB['embedding'])

    dot_product = np.dot(vectorA, vectorB)
    normA = np.linalg.norm(vectorA)
    normB = np.linalg.norm(vectorB)
    return dot_product / (normA * normB)

def calculate_cosine_similarities(embeddings):
    num_embeddings = len(embeddings)
    similarities = np.zeros((num_embeddings, num_embeddings))

    for i in range(num_embeddings):
        for j in range(i, num_embeddings):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            similarities[i, j] = sim
            similarities[j, i] = sim

    return similarities

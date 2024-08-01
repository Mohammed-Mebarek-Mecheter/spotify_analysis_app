from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def create_embeddings(data):
    song_embeddings = []
    for _, row in data.iterrows():
        text = f"{row['Track']} by {row['Artist']} from {row['Album Name']}"
        embedding = get_embedding(text)
        song_embeddings.append(embedding)
    return np.array(song_embeddings)

def get_recommendations(query, data, song_embeddings, n=5):
    query_embedding = get_embedding(query)
    similarities = cosine_similarity([query_embedding], song_embeddings)[0]
    top_indices = similarities.argsort()[-n:][::-1]
    return data.iloc[top_indices]
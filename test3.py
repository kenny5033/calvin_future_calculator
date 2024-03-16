from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

# Load pre-trained model
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Load datasets
subject_data = pd.read_csv('/Users/lillianmcaboy/Desktop/fineTuning.csv')
class_data = pd.read_csv('/Users/lillianmcaboy/Desktop/classes.csv')

class_data["Class Name"] = class_data["Department"] + class_data["Class"].astype(str)

# Generate embeddings for subject descriptions
subject_embeddings = model.encode(subject_data['Description'].tolist(), convert_to_tensor=True)

# Generate initial embeddings for class descriptions
class_embeddings = model.encode(class_data['Description'].tolist(), convert_to_tensor=True)

# Fine-tune class embeddings towards subject embeddings
learning_rate = 0.01
num_epochs = 10
for epoch in range(num_epochs):
    for class_idx in range(len(class_embeddings)):
        class_embedding = class_embeddings[class_idx].unsqueeze(0)  # Add batch dimension
        similarity = util.pytorch_cos_sim(class_embedding, subject_embeddings)[0]
        max_similarity_idx = torch.argmax(similarity)
        anchor_embedding = subject_embeddings[max_similarity_idx].unsqueeze(0)  # Add batch dimension
        class_embeddings[class_idx] += learning_rate * (anchor_embedding - class_embedding).squeeze(0)

# Stack class embeddings into a single tensor
class_embeddings_stacked = torch.stack(tuple(class_embeddings))

# Get user input
user_input = input("Enter a subject description: ")

# Encode user input
user_embedding = model.encode(user_input, convert_to_tensor=True)

# Calculate similarity between user input and class embeddings
similarities = util.pytorch_cos_sim(user_embedding, class_embeddings_stacked)

# Find the most similar class

top_indices = torch.topk(similarities, k=3).indices.tolist()

print(f"The top 3 classes most similar to '{user_input}':")
for idx in top_indices:
    class_name = class_data.loc[idx, 'Class Name']
    class_description = class_data.loc[idx, 'Description']
    similarity_score = similarities[0, idx]
    print(f"\nClass Name: \n{class_name}, Similarity Score: {similarity_score}")
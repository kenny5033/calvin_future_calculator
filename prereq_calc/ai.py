from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

# server neccessary imports
import sys
import json
from os import getcwd

# Load pre-trained model
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Load datasets
subject_data = pd.read_csv(f'{getcwd()}/data/fineTuning.csv')
class_data = pd.read_csv(f'{getcwd()}/data/classes.csv')

class_data["Class Name"] = class_data["Department"] + class_data["Class"].astype(str)
class_data["NameAndDescr"] = class_data["Name"] + class_data["Description"]

# Generate embeddings for subject descriptions
subject_embeddings = model.encode(subject_data['Description'].tolist(), convert_to_tensor=True)

# Generate initial embeddings for class descriptions
class_embeddings = model.encode(class_data['NameAndDescr'].tolist(), convert_to_tensor=True)

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
user_input = sys.argv[1]

# Encode user input
user_embedding = model.encode(user_input, convert_to_tensor=True)

# Calculate similarity between user input and class embeddings
similarities = util.pytorch_cos_sim(user_embedding, class_embeddings_stacked)

# Find the most similar class

top_indices = torch.topk(similarities, k=3).indices.tolist()

# print(f"The top 3 classes most similar to '{user_input}':")
# for idx in top_indices:
#     class_name = class_data.loc[idx, 'Class Name']
#     class_description = class_data.loc[idx, 'Description']
#     similarity_score = similarities[0, idx]
#     print(f"\nClass Name: \n{class_name}, Similarity Score: {similarity_score}")

# Server designed output (json)
act_top_indices = top_indices[0] # top_indicies is a list inside a list, this removes the first list
print(json.dumps(
    {
        "top_choice": class_data.loc[act_top_indices[0], 'Class Name'],
        "second_choice": class_data.loc[act_top_indices[1], 'Class Name'],
        "third_choice": class_data.loc[act_top_indices[2], 'Class Name']
    }
))
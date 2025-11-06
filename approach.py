import pandas as pd
import ast
from sentence_transformers import SentenceTransformer, util
import torch

# Load data
df = pd.read_csv('/home/geniusff/chaitnya/TEAM-G-Kernel-boot/coursera_courses.csv')

# Parse skills
def parse_list(x):
    try:
        return ' '.join(ast.literal_eval(x))
    except:
        return str(x)
df['course_skills'] = df['course_skills'].apply(parse_list)

# Combine text fields
df['text'] = df['course_title'] + ' ' + df['course_skills'] + ' ' + df['course_summary'] + ' ' + df['course_description']

# Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['text'], convert_to_tensor=True)

# User input
user_input = "i want to learn about data science and ai techniques used in drone technology"
user_embedding = model.encode([user_input], convert_to_tensor=True)

# Compute similarity
cosine_scores = util.cos_sim(user_embedding, embeddings)[0]

# Top 5
top_results = torch.topk(cosine_scores, k=5)
print(top_results)
for idx, score in zip(top_results[1], top_results[0]):
    i = int(idx)   # convert tensor to integer
    print(f"\nCourse: {df.iloc[i]['course_title']}")
    print(f"Score: {score:.4f}")
    print(f"Organization: {df.iloc[i]['course_organization']}")
    print(f"Skills: {df.iloc[i]['course_skills']}")
    print(f"URL: {df.iloc[i]['course_url']}")


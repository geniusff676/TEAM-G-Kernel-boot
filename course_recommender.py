from flask import Flask, request, jsonify
import pandas as pd
import ast
from sentence_transformers import SentenceTransformer, util
import torch
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# ======== Load Data and Model Once ========

# Load dataset
df = pd.read_csv('/home/geniusff/chaitnya/TEAM-G-Kernel-boot/coursera_courses.csv')

# Parse skills column safely
def parse_list(x):
    try:
        return ' '.join(ast.literal_eval(x))
    except:
        return str(x)

df['course_skills'] = df['course_skills'].apply(parse_list)

# Combine text fields into one column
df['text'] = (
    df['course_title'].astype(str) + ' ' +
    df['course_skills'].astype(str) + ' ' +
    df['course_summary'].astype(str) + ' ' +
    df['course_description'].astype(str)
)

# Load SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings for all courses
embeddings = model.encode(df['text'].tolist(), convert_to_tensor=True)

# ======== API Endpoint ========

@app.route('/recommend', methods=['POST'])
def recommend_courses():
    data = request.get_json()
    user_input = data.get("query", "")

    if not user_input.strip():
        return jsonify({"error": "Empty input query"}), 400

    # Encode user input
    user_embedding = model.encode([user_input], convert_to_tensor=True)

    # Compute cosine similarity
    cosine_scores = util.cos_sim(user_embedding, embeddings)[0]

    # Get top 3 results
    top_results = torch.topk(cosine_scores, k=3)

    # Prepare response
    recommendations = []
    for idx, score in zip(top_results[1], top_results[0]):
        i = int(idx)
        recommendations.append({
            "course_title": df.iloc[i]['course_title'],
            "organization": df.iloc[i]['course_organization'],
            "skills": df.iloc[i]['course_skills'],
            "url": df.iloc[i]['course_url'],
            "similarity_score": round(float(score), 4)
        })

    return jsonify({
        "query": user_input,
        "top_courses": recommendations
    })

# ======== Run Server ========

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

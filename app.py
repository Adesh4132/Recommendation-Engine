from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Sample data (movies/products)
items = pd.DataFrame([
    {"id": 1, "name": "Inception", "genre": "Sci-Fi", "features": [1,0,0,1,0]},
    {"id": 2, "name": "The Matrix", "genre": "Sci-Fi", "features": [1,0,1,1,0]},
    {"id": 3, "name": "Titanic", "genre": "Romance", "features": [0,1,0,0,1]},
    {"id": 4, "name": "The Notebook", "genre": "Romance", "features": [0,1,0,0,1]},
    {"id": 5, "name": "John Wick", "genre": "Action", "features": [1,0,1,0,0]},
])

# Dummy user-item ratings matrix
user_item_ratings = pd.DataFrame([
    {"user_id": 1, "item_id": 1, "rating": 5},
    {"user_id": 1, "item_id": 2, "rating": 4},
    {"user_id": 2, "item_id": 3, "rating": 5},
    {"user_id": 2, "item_id": 4, "rating": 4},
    {"user_id": 3, "item_id": 5, "rating": 5},
])

def content_based_recommendations(item_id, top_n=3):
    # Content-based filtering using cosine similarity
    item_vecs = np.stack(items['features'])
    idx = items[items['id'] == item_id].index[0]
    sim_scores = cosine_similarity([item_vecs[idx]], item_vecs)[0]
    similar_indices = sim_scores.argsort()[::-1][1:top_n+1]
    recs = items.iloc[similar_indices][['id', 'name', 'genre']]
    return recs.to_dict(orient='records')

def collaborative_recommendations(user_id, top_n=3):
    # Collaborative filtering: user-based (very basic)
    pivot = user_item_ratings.pivot(index="user_id", columns="item_id", values="rating").fillna(0)
    if user_id not in pivot.index:
        return []
    target_ratings = pivot.loc[user_id].values
    user_sims = cosine_similarity([target_ratings], pivot.values)[0]
    top_users = pivot.index[user_sims.argsort()[::-1][1:top_n+1]]
    recommended_items = []
    for neighbor in top_users:
        neighbor_rated = pivot.loc[neighbor]
        for item in neighbor_rated.index:
            if target_ratings[item-1] == 0 and neighbor_rated[item] > 0:
                recommended_items.append(item)
    recommended_items = list(set(recommended_items))
    recs = items[items['id'].isin(recommended_items)][['id', 'name', 'genre']]
    return recs.to_dict(orient='records')

@app.route("/recommend/content", methods=["GET"])
def recommend_content():
    item_id = int(request.args.get("item_id"))
    top_n = int(request.args.get("top_n", 3))
    recs = content_based_recommendations(item_id, top_n)
    return jsonify({"recommendations": recs})

@app.route("/recommend/collaborative", methods=["GET"])
def recommend_collaborative():
    user_id = int(request.args.get("user_id"))
    top_n = int(request.args.get("top_n", 3))
    recs = collaborative_recommendations(user_id, top_n)
    return jsonify({"recommendations": recs})

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items[["id","name","genre"]].to_dict(orient="records"))

@app.route("/users", methods=["GET"])
def get_users():
    users = user_item_ratings["user_id"].unique().tolist()
    return jsonify({"users": users})

if __name__ == "__main__":
    app.run(debug=True)
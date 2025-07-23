import streamlit as st
import pickle
import httpx
import os
import time
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

# Load data
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '../data-pkl/movies.pkl')


with open(file_path, 'rb') as f:
    movies = pickle.load(f)

similarity = pickle.load(open('../data-pkl/similarity.pkl', 'rb'))

# Fetch poster using TMDB API
def fetch_poster(movie_id):
    url =  f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    headers = {
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                return "https://via.placeholder.com/500x750.png?text=No+Image"
    except Exception as e:
        print("❌ Failed to fetch poster:", e)
        return "https://via.placeholder.com/500x750.png?text=No+Image"

# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # fetch correct movie_id (not index)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        time.sleep(0.3)  # rate limit
    return recommended_movies, recommended_posters

# ================================
# STREAMLIT UI
# ================================
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Choose your Favorite Movie",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.subheader("Top 5 Recommendations:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])

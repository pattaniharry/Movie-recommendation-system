import streamlit as st
import pickle
import requests

from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")  


# Load the full movies DataFrame
movies = pickle.load(open('../data-pkl/movies.pkl', 'rb'))
similarity = pickle.load(open('../data-pkl/similarity.pkl', 'rb'))
  #to fetch poster 
import httpx
import time

def fetch_poster(movie_id):


    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Mozilla/5.0"  # Helps prevent TMDB rejecting request
    }

    
    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500" + data['poster_path']


   
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = i[0]

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

# UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Choose your Favorite Movie",
    movies['title'].values  # Use titles for dropdown
)

if st.button('Recommend'):
    name, posters = recommend(selected_movie_name)
    st.subheader("Top 5 Recommendations:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")


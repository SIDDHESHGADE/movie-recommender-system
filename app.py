import pickle
import streamlit as st
import gdown
import os

st.set_page_config(page_title='Movie Recommender System', page_icon="🤖", layout="centered")

# Google Drive File IDs (Extracted Correctly)
movie_list_file_id = "1qTgxqyurjXg9Rt-yGarJSYioGrpKhN6V"
similarity_file_id = "1--JYrE02iOtOa8CDLeLtQVje4R_6YFvU"

# Filenames
movie_list_path = "movie_list.pkl"
similarity_path = "similarity.pkl"

# Function to download files from Google Drive
def download_file(file_id, output):
    if not os.path.exists(output):  # Avoid re-downloading if the file exists
        with st.spinner(f"Downloading {output}..."):
            url = f"https://drive.google.com/uc?export=download&id={file_id}"  # Corrected download link
            gdown.download(url, output, quiet=False)

# Download the pickle files if they don't exist
download_file(movie_list_file_id, movie_list_path)
download_file(similarity_file_id, similarity_path)

# Load the pickled data
movies = pickle.load(open(movie_list_path, "rb"))
similarity = pickle.load(open(similarity_path, "rb"))

# Movie Recommendation Function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = [movies.iloc[i[0]].title for i in distances[1:6]]
    return recommended_movie_names

st.header('🎬 Movie Recommender System')

# Dropdown to select a movie
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)

    st.write("### Recommended Movies:")
    for i, movie in enumerate(recommended_movie_names, start=1):
        st.write(f"**{i}. {movie}**")  # Displays numbered list

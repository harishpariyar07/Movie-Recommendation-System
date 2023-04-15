import streamlit as st
import pickle
import pandas as pd
import requests
from pathlib import Path

import streamlit_authenticator as stauth


# ---USER AUTHENTICATION---

names = ["Harish Pariyar", "Veni Tiwari", "Rishi Sharma",
         "Anadya Sahai", "Suvidha Srivastva", "Sachin Kansal"]
usernames = ["hpariyar", "vtiwari", "rsharma",
             "asahai", "ssrivastva", "skansal"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords, "movie_recommendation_system", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username or Password is incorrect")
if authentication_status == None:
    st.warning("Please enter your username and password")
if authentication_status:

    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=f9a4b5ee10590804fd30f6d6241e9838&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    def recommend(movie):
        movie_index = movies[movies['original_title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)),
                             reverse=True, key=lambda x: x[1])[1:6]

        recommended_movie_names = []
        recommended_movie_posters = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].id
            # fetch posters from API
            recommended_movie_posters.append(fetch_poster(movie_id))
            # fetch movie names
            recommended_movie_names.append(movies.iloc[i[0]].original_title)
        return recommended_movie_names, recommended_movie_posters

    st.title('Movie Recommendation System')
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    selected_movie_name = st.selectbox(
        'Which movie would you like to get recommendations for?',
        movies['original_title'].values


    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(
            selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])

        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.header("Options")

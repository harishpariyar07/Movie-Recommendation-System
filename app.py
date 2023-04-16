import streamlit_authenticator as stauth
import streamlit as st
import pickle
import pandas as pd
import requests
from pathlib import Path
textColor = "#7fffd4"


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

    def fetch_imdb_id(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=f9a4b5ee10590804fd30f6d6241e9838&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        imdb_id = data['imdb_id']
        return imdb_id

    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies_dict2 = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    movies2 = pd.DataFrame(movies_dict2)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    imdb_dict = pickle.load(open('imdb.pkl', 'rb'))
    imdb = pd.DataFrame(imdb_dict)

    def recommend(movie):
        movie_index = movies[movies['original_title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)),
                             reverse=True, key=lambda x: x[1])[1:6]

        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_overview = []
        recommended_movie_imdbRating = []
        imdbID = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].id
            # fetch posters from API
            recommended_movie_posters.append(fetch_poster(movie_id))
            imdb_id = fetch_imdb_id(movie_id)
            imdbID.append(imdb_id)
            # fetch movie names
            recommended_movie_names.append(movies.iloc[i[0]].original_title)
            recommended_movie_overview.append(movies2.iloc[i[0]].overview)
            recommended_movie_imdbRating.append(
                imdb.loc[imdb['tconst'] == imdb_id, 'averageRating'].item())
        return recommended_movie_names, recommended_movie_posters, recommended_movie_overview, recommended_movie_imdbRating, imdbID

    st.title('Movie Recommendation System')

    selected_movie_name = st.selectbox(
        'Which movie would you like to get recommendations for?',
        movies['original_title'].values
    )

    if st.button('Show Recommendations',):
        recommended_movie_names, recommended_movie_posters, recommended_movie_overview, recommended_movie_imdbRating, imdbID = recommend(
            selected_movie_name)

        col1, col2 = st.columns(2)
        with col1:
            url = "https://www.imdb.com/title/" + imdbID[0]
            recommended_movie_names[0] = '[' + \
                recommended_movie_names[0]+'](%s)' % url
            st.subheader(recommended_movie_names[0])
            st.write('IMDb Rating: ', recommended_movie_imdbRating[0])
            st.write(" ".join(recommended_movie_overview[0]))
        with col2:
            with st.columns(3)[1]:
                st.image(recommended_movie_posters[0], width=225)
        st.write("---")

        col1, col2 = st.columns(2)
        with col1:
            url = "https://www.imdb.com/title/" + imdbID[1]
            recommended_movie_names[1] = '[' + \
                recommended_movie_names[1]+'](%s)' % url
            st.subheader(recommended_movie_names[1])
            st.write('IMDb Rating: ', recommended_movie_imdbRating[1])
            st.write(" ".join(recommended_movie_overview[1]))
        with col2:
            with st.columns(3)[1]:
                st.image(recommended_movie_posters[1], width=225)
        st.write("---")

        col1, col2 = st.columns(2)
        with col1:
            url = "https://www.imdb.com/title/" + imdbID[2]
            recommended_movie_names[2] = '[' + \
                recommended_movie_names[2]+'](%s)' % url
            st.subheader(recommended_movie_names[2])
            st.write('IMDb Rating: ', recommended_movie_imdbRating[2])
            st.write(" ".join(recommended_movie_overview[2]))
        with col2:
            with st.columns(3)[1]:
                st.image(recommended_movie_posters[2], width=225)
        st.write("---")

        col1, col2 = st.columns(2)
        with col1:
            url = "https://www.imdb.com/title/" + imdbID[3]
            recommended_movie_names[3] = '[' + \
                recommended_movie_names[3]+'](%s)' % url
            st.subheader(recommended_movie_names[3])
            st.write('IMDb Rating: ', recommended_movie_imdbRating[3])
            st.write(" ".join(recommended_movie_overview[3]))
        with col2:
            with st.columns(3)[1]:
                st.image(recommended_movie_posters[3], width=225)
        st.write("---")

        col1, col2 = st.columns(2)
        with col1:
            url = "https://www.imdb.com/title/" + imdbID[4]
            recommended_movie_names[4] = '[' + \
                recommended_movie_names[4]+'](%s)' % url
            st.subheader(recommended_movie_names[4])
            st.write('IMDb Rating: ', recommended_movie_imdbRating[4])
            st.write(" ".join(recommended_movie_overview[4]))
        with col2:
            with st.columns(3)[1]:
                st.image(recommended_movie_posters[4], width=225)
        st.write("---")

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.header("Options")

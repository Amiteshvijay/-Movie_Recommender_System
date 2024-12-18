from flask import Flask, render_template, request
import pandas as pd
import pickle as pkl
import requests

app = Flask(__name__)

# Store the API key in a variable
api_key = '16c1f3a518b5c4506e7bca7ef3f1e86c'


# Function to fetch movie posters from the TMDB API
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')
    data = response.json()
    poster_path = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    return poster_path


# Function to recommend movies with exception handling
def recommend(movie):
    try:
        if not movie:  # Check if the movie title is empty or None
            raise ValueError("Movie title cannot be empty.")

        recommended_movies = []
        recommended_movies_poster = []
        recommended_movies_website = []
        movie_index = movies[movies['title'] == movie].index[0]  # Could raise IndexError if movie not found
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        for i in movie_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_poster

    except IndexError:
        return "Movie not found. Please check the title and try again."

    except ValueError as ve:
        return str(ve)

    except Exception as e:
        return f"An error occurred: {str(e)}"


# Load the movies and similarity data
movies = pkl.load(open('movies.pkl', 'rb'))
similarity = pkl.load(open('similarity.pkl', 'rb'))


@app.route('/', methods=['GET', 'POST'])
def home():
    recommended_movies = []
    recommended_movies_poster = []
    selected_movie = None

    if request.method == 'POST':
        selected_movie = request.form['movie_name']
        recommended_movies, recommended_movies_poster = recommend(selected_movie)


    # Render the HTML template and pass data
    return render_template('index.html', movies=movies['title'].values,selected_movie_name=selected_movie,
                           recommended_movies=recommended_movies, posters=recommended_movies_poster, zip=zip)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)

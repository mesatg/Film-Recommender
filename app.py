from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import requests

app = Flask(__name__)

API_KEY = 'b38a1d89382721590ac0c691832bed08'
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# Veri setlerini yükle
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, left_on='id', right_on='movie_id')

if 'original_title' in movies.columns:
    movies.rename(columns={'original_title': 'title'}, inplace=True)

movies = movies[['title', 'overview', 'genres', 'keywords', 'cast', 'crew']].dropna()

def get_movie_poster(title):
    response = requests.get(f"{BASE_URL}/search/movie", params={'api_key': API_KEY, 'query': title})
    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return IMAGE_BASE_URL + poster_path
    return '/static/images/default_poster.png'

def process_data():
    def get_director(crew):
        for member in ast.literal_eval(crew):
            if member['job'] == 'Director':
                return member['name']
        return ''

    def get_top_cast(cast):
        return [member['name'] for member in ast.literal_eval(cast)[:3]]

    def get_list(obj):
        return [item['name'] for item in ast.literal_eval(obj)]

    movies['director'] = movies['crew'].apply(get_director)
    movies['cast'] = movies['cast'].apply(get_top_cast)
    movies['genres'] = movies['genres'].apply(get_list)
    movies['keywords'] = movies['keywords'].apply(get_list)

    def collapse(x):
        return " ".join(x).replace(" ", "").lower()

    movies['cast'] = movies['cast'].apply(collapse)
    movies['genres'] = movies['genres'].apply(collapse)
    movies['keywords'] = movies['keywords'].apply(collapse)
    movies['director'] = movies['director'].apply(lambda x: x.replace(" ", "").lower())
    movies['tags'] = movies['overview'].apply(lambda x: x.lower()) + " " + movies['genres'] + " " + movies['keywords'] + " " + movies['cast'] + " " + movies['director']

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity

similarity = process_data()

df_titles = movies['title'].str.lower().tolist()

@app.route('/')
def home():
    return render_template('index.html', movies=list(movies['title'].values))

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').lower()
    suggestions = [title for title in df_titles if query in title][:5]
    return jsonify(suggestions)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.json.get('movie').lower()
    if movie not in movies['title'].str.lower().values:
        return jsonify({'error': 'Film bulunamadı.'})
    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    main_poster = get_movie_poster(movies.iloc[index].title)
    recommended = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster = get_movie_poster(title)
        recommended.append({'title': title, 'poster': poster})

    return jsonify({'main_poster': main_poster, 'recommended': recommended})

if __name__ == '__main__':
    app.run(debug=True)
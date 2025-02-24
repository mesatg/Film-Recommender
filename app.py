from flask import Flask, render_template, request, jsonify
import joblib
import requests

app = Flask(__name__)

API_KEY = 'b38a1d89382721590ac0c691832bed08'
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# 🎬 Eğitilen modeli yükle
movies, similarity = joblib.load('film_recommender_model.pkl')
df_titles = movies['original_title'].str.lower().tolist()

# 🎞️ Film posteri alma fonksiyonu
def get_movie_poster(title):
    try:
        response = requests.get(
            f"{BASE_URL}/search/movie",
            params={'api_key': API_KEY, 'query': title}
        )
        data = response.json()
        if 'results' in data and data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return IMAGE_BASE_URL + poster_path
        return '/static/images/default_poster.png'
    except Exception as e:
        print(f"🚨 API hatası: {e}")
        return '/static/images/default_poster.png'

# 🌐 Ana sayfa
@app.route('/')
def home():
    return render_template('index.html', movies=list(movies['original_title'].values))

# 🔍 Otomatik tamamlama
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').lower()
    suggestions = [title for title in df_titles if query in title][:5]
    return jsonify(suggestions)

# 🎥 Film önerme
@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.json.get('movie').lower()
    if movie not in movies['original_title'].str.lower().values:
        return jsonify({'error': 'Film bulunamadı.'})
    index = movies[movies['original_title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    main_poster = get_movie_poster(movies.iloc[index].original_title)
    recommended = []
    for i in movies_list:
        title = movies.iloc[i[0]].original_title
        poster = get_movie_poster(title)
        recommended.append({'title': title, 'poster': poster})

    return jsonify({'main_poster': main_poster, 'recommended': recommended})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

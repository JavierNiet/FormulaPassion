from flask import Flask, jsonify
from flask_cors import CORS
import feedparser
import os

app = Flask(__name__)
CORS(app)

def fetch_f1_news():
    # RSS de Motorsport en español e inglés
    feeds = {
        'es': 'https://lat.motorsport.com/rss/f1/news/',
        'en': 'https://www.motorsport.com/rss/f1/news/'
    }
    news = {'es': [], 'en': []}
    for lang, url in feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:  # Solo los 10 más recientes
            news[lang].append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published if 'published' in entry else ''
            })
    return news

# Endpoint para noticias (español e inglés)
@app.route('/api/news', methods=['GET'])
def get_news():
    news = fetch_f1_news()
    return jsonify(news)

# Endpoint para resultados de carreras
@app.route('/api/results', methods=['GET'])
def get_results():
    # Aquí se integrarán resultados de carreras
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5003)

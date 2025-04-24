from flask import Flask, jsonify, request, send_from_directory
from news_extract import summarize_article
from news_scrape import get_article_urls, my_url
from news_nlp import find_sentiment
from textblob import TextBlob
import threading
import json
import os
import time
import re

app = Flask(__name__, static_folder='.')

# In-memory storage for articles
articles_data = []
is_scraping = False

# Path for the scraped articles JSON file
SCRAPED_ARTICLES_JSON = 'scraped_articles.json'

def get_sentiment_values(text):
    """Extract polarity and subjectivity values from text"""
    analysis = TextBlob(text)
    return {
        "polarity": round(analysis.sentiment.polarity, 2),
        "subjectivity": round(analysis.sentiment.subjectivity, 2)
    }

def extract_title_from_url(url):
    """Extract a readable title from the URL"""
    path = url.split('/')[-1]
    path = path.replace('.html', '')
    title = path.replace('-', ' ').title()
    return title

def save_to_json(articles):
    """Save scraped articles to a JSON file"""
    with open(SCRAPED_ARTICLES_JSON, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(articles)} articles to {SCRAPED_ARTICLES_JSON}")

def load_from_json():
    """Load scraped articles from JSON file"""
    if os.path.exists(SCRAPED_ARTICLES_JSON):
        try:
            with open(SCRAPED_ARTICLES_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading from JSON: {e}")
    return []

def scrape_articles(browser="firefox"):
    """Scrape articles in the background"""
    global articles_data, is_scraping
    
    if is_scraping:
        return {"status": "already_running"}
    
    is_scraping = True
    
    try:
        print(f"Starting scraping with {browser}...")
        urls = get_article_urls(my_url, browser)
        print(f"Found {len(urls)} URLs to process")
        
        existing_urls = set()
        new_articles = []
        
        saved_articles = load_from_json()
        if saved_articles:
            for article in saved_articles:
                if "url" in article:
                    existing_urls.add(article["url"])
            new_articles = saved_articles.copy()
        
        processed_count = 0
        for url in urls:
            if url in existing_urls:
                continue
                
            if processed_count >= 40:
                break
                
            try:
                print(f"Processing article: {url}")
                summary = summarize_article(url)
                sentiment = get_sentiment_values(summary)
                title = extract_title_from_url(url)
                
                from newspaper import Article
                article_obj = Article(url)
                try:
                    article_obj.download()
                    article_obj.parse()
                    top_image = article_obj.top_image
                except:
                    top_image = ""
                
                article = {
                    "title": title,
                    "summary": summary,
                    "polarity": sentiment["polarity"],
                    "subjectivity": sentiment["subjectivity"],
                    "url": url,
                    "author": "New York Times",
                    "image_url": top_image,
                    "timestamp": time.time()
                }
                
                new_articles.append(article)
                existing_urls.add(url)
                processed_count += 1
                print(f"Added article: {title}")
            except Exception as e:
                print(f"Error processing article {url}: {e}")
    
    except Exception as e:
        print(f"Error scraping articles: {e}")
    
    finally:
        is_scraping = False
        
        if new_articles:
            new_articles.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
            
            unique_articles = []
            seen_urls = set()
            
            for article in new_articles:
                if article.get('url') not in seen_urls:
                    unique_articles.append(article)
                    seen_urls.add(article.get('url'))
            
            articles_data = unique_articles
            save_to_json(unique_articles)
            print(f"Scraping completed, saved {len(unique_articles)} unique articles")
        else:
            print("No new articles were found")
    
    return {"status": "completed", "count": processed_count}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/news')
def get_news():
    page = request.args.get('page', default=1, type=int)
    
    if not articles_data:
        loaded_articles = load_from_json()
        if loaded_articles:
            start_index = (page - 1) * 20
            end_index = start_index + 20
            return jsonify(loaded_articles[start_index:end_index])
        
        try:
            with open('data.js', 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'const newsData = (\[.*?\]);', content, re.DOTALL)
                if match:
                    sample_data = json.loads(match.group(1))
                    threading.Thread(target=scrape_articles).start()
                    start_index = (page - 1) * 20
                    end_index = start_index + 20
                    return jsonify(sample_data[start_index:end_index])
        except Exception as e:
            print(f"Error loading sample data: {e}")
            
        threading.Thread(target=scrape_articles).start()
        return jsonify([])
    
    start_index = (page - 1) * 20
    end_index = start_index + 20
    return jsonify(articles_data[start_index:end_index])

@app.route('/api/refresh', methods=['POST'])
def refresh_news():
    browser = request.args.get('browser', 'firefox')
    threading.Thread(target=scrape_articles, args=(browser,)).start()
    return jsonify({"status": "scraping_started"})

if __name__ == '__main__':
    print("News Aggregator Server Starting...")
    print("Open http://127.0.0.1:5000 in your browser")
    
    saved_articles = load_from_json()
    if saved_articles:
        articles_data = saved_articles
        print(f"Loaded {len(articles_data)} articles from {SCRAPED_ARTICLES_JSON}")
    
    app.run(debug=True)
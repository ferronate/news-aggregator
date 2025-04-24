# News Aggregator: NY Times Tech News Analyzer

A web application that scrapes technology articles from The New York Times, performs sentiment analysis on their content, and presents them in an interactive interface with expandable cards showing polarity and objectivity metrics.

---

## Features

- **Automated News Scraping**: Collects the latest technology articles from the New York Times.
- **Sentiment Analysis**: Analyzes text for polarity (positive/negative) and subjectivity (factual/opinion).
- **Interactive UI**:
  - Expandable article cards with summary and full view.
  - Sentiment visualization sliders.
  - Thumbnail and full-size article images.
- **Dark Mode**: Toggle between light and dark themes.
- **Search Functionality**: Find articles by keyword.
- **Pagination**: Navigate through multiple pages of articles.
- **Refresh Content**: One-click update to fetch new articles.

---

## Technologies Used

- **Backend**: Flask, Python
- **Web Scraping**: Selenium, Newspaper3k
- **NLP**: TextBlob for sentiment analysis
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Data Storage**: JSON file persistence

---

## Installation

### Prerequisites

- Python 3.9+
- Web browser (Chrome, Firefox, Edge, or Brave)
- Required Python libraries (see `requirements.txt`)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ferronate/news-aggregator.git
   cd news-aggregator
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **WebDriver setup**:
   - Ensure you have the appropriate browser installed (Firefox recommended).
   - The `webdriver-manager` library should handle driver installation automatically.

---

## Usage

1. **Start the Flask server**:
   ```bash
   python server.py
   ```

2. **Open your web browser** and navigate to the provided URL.

### User Interface:

- Click an article card to expand and see full content.
- Use the refresh button to fetch new articles.
- Toggle dark mode with the sun/moon button.
- Search articles using the search box.

---

## Project Structure

- `server.py` - Flask server and main application logic.
- `news_scrape.py` - Web scraping functionality.
- `news_extract.py` - Article extraction and summarization.
- `news_nlp.py` - Sentiment analysis functions.
- `scraped_articles.json` - Persistent storage for scraped articles.
- `index.html` - Frontend user interface.
- `script.js` - Frontend JavaScript functionality.
- `styles.css` - Styling and theming.
- `main.py` - Command-line interface for testing.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **New York Times** for providing the article content.
- **TextBlob** for sentiment analysis capabilities.
- **Newspaper3k** for article extraction.

---

### Note:

This project is for educational purposes only. Please respect the New York Times' terms of service when scraping content.

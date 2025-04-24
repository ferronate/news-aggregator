from newspaper import Article

def summarize_article(url):
    article = Article(url)

    try:
        article.download()
        article.parse()
        article.nlp()
    except Exception as e:
        print(f"Failed to process article at {url}: {e}")
        return "Summary not available"

    author_string = "Author(s): " + ", ".join(article.authors) if article.authors else "Author(s): Not available"
    print(author_string)

    date = article.publish_date
    print("Publish Date:", date.strftime("%m/%d/%Y") if date else "Not available")

    print("Top Image URL:", article.top_image)
    print(f"Total Images Found: {len(article.images)}")
    for i, image in enumerate(list(article.images)[:3]):
        print(f"\tImage {i + 1}: {image}")
    
    print("\nA Quick Article Summary")
    print("----------------------------------------")
    print(article.summary)

    return article.summary

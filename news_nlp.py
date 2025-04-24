from textblob import TextBlob

def find_sentiment(news_story):
    news = TextBlob(news_story)

    polarity_data = []
    subjectivity_data = []

    for sentence in news.sentences:
        polarity_data.append(sentence.sentiment.polarity)
        subjectivity_data.append(sentence.sentiment.subjectivity)

    polarity_average = calculate_average(polarity_data)
    subjectivity_average = calculate_average(subjectivity_data)

    print("\nFINAL ANALYSIS")
    print("----------------------------------")
    print("Polarity:", calculate_sentiment(polarity_average, "polarity"))
    print("Subjectivity:", calculate_sentiment(subjectivity_average, "subjectivity"))

def calculate_average(lst):
    return sum(lst) / len(lst) if lst else 0

def calculate_sentiment(sentiment, type):
    if type == "polarity":
        if sentiment > 0.75:
            return "Extremely positive."
        elif sentiment > 0.5:
            return "Significantly positive."
        elif sentiment > 0.3:
            return "Fairly positive."
        elif sentiment > 0.1:
            return "Slightly positive."
        elif sentiment < -0.75:
            return "Extremely negative."
        elif sentiment < -0.5:
            return "Significantly negative."
        elif sentiment < -0.3:
            return "Fairly negative."
        elif sentiment < -0.1:
            return "Slightly negative."
        else:
            return "Neutral."
    elif type == "subjectivity":
        if sentiment > 0.75:
            return "Extremely subjective."
        elif sentiment > 0.5:
            return "Fairly subjective."
        elif sentiment > 0.3:
            return "Fairly objective."
        elif sentiment > 0.1:
            return "Extremely objective."
        else:
            return "Completely objective."
    else:
        return "Invalid input."

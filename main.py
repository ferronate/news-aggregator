# Imports all the methods and variables from each script.
from news_extract import *
from news_scrape import *
from news_nlp import *
import time

# Welcome Messages and Introduction
print("Welcome to the Newspaper Scrape Project. \nIn seconds, you will have access to the latest articles "
      "in the technology section of the New York Times. \nIn addition, you will also be able to know whether the "
      "article is positive or negative and the extent of the writer's bias.")
print()

# Getting the user input; adding an element of personalization!
name = input("Enter your name to get started: ")

# Add this after the name input to let users choose their browser
browser_choice = input("Select a browser (chrome, edge, firefox, brave): ").lower()
if browser_choice not in ["chrome", "edge", "firefox", "brave"]:
    print(f"Invalid browser choice: {browser_choice}. Using Chrome as default.")
    browser_choice = "chrome"

# Console Display
print("Welcome " + name + "! \nYou will now see the latest technology articles in the New York Times...")
print("Extracting article hyperlinks...")
time.sleep(2)
print("Retrieving summaries...")
print()
time.sleep(2)

# Get all URLs from the NY Times Technology Section
# Replace this section in your main.py

# Gets all the latest URLs from the NY Times Technology Section (from Selenium method)
url_list = get_article_urls(my_url, browser_choice)

# Use the correct article URLs and process each article
for url in url_list:
    print("Article URL: " + str(url))  # Print the actual article URL
    article_summary = summarize_article(url)  # Summarize the article using the correct URL
    find_sentiment(article_summary)  # Perform sentiment analysis on the article summary
    print("------------------------------------------------")
    time.sleep(7)  # Allows user to get through all the text.


# Closing Messages
print()
print("The articles have been successfully extracted!")
print("In total, we were able to extract " + str(len(url_list)) + " different articles!")
print("Thanks for participating, " + name + "!")

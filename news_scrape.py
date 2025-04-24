from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

my_url = "https://www.nytimes.com/section/technology"

def get_article_urls(url, browser="chrome"):
    """
    Scrape article URLs from the given URL using the specified browser.
    
    Parameters:
    - url: URL to scrape
    - browser: Browser to use ('chrome', 'edge', 'firefox', 'brave')
    
    Returns:
    - List of article URLs
    """
    browser = browser.lower()
    
    if browser == "chrome":
        options = ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    elif browser == "edge":
        options = EdgeOptions()
        options.headless = True
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    
    elif browser == "firefox" or browser == "zen":
        options = FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    
    elif browser == "brave":
        options = ChromeOptions()
        options.headless = True
        options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.get(url)

    try:
        # Wait for the page to load and find article links
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/2025/']")))

        # Try using a more specific CSS selector
        articles = driver.find_elements(By.CSS_SELECTOR, "a[href*='/2025/']")

        # Collect article URLs while ensuring they are valid
        article_urls = list(set([
            a.get_attribute("href")
            for a in articles
            if a.get_attribute("href") and "/technology/" in a.get_attribute("href")
        ]))

        if not article_urls:
            print("No article URLs found.")
        else:
            print(f"Found {len(article_urls)} articles.")

    except Exception as e:
        print(f"Error while scraping articles: {e}")
        article_urls = []

    finally:
        driver.quit()  # Always close the browser at the end

    return article_urls

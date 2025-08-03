#--------------------------------

# Imports
import re
from selenium import webdriver
from bs4 import BeautifulSoup
#--------------------------------

def snippet_strippet(raw_text):
    """
    strip trip for the snip ship
    """
    text = raw_text.get_text(" ", strip=True)

    # remove symbols
    text = re.sub(r"[ⓘ■◆●►]", "", text)

    # strip reference markers like [1], [23], etc.
    text = re.sub(r"\[\d+\]", "", text)

    # strip timestamps on article updates
    text = re.sub(r"\b\d+\s+(seconds?|minutes?|hours?|days?|weeks?|months?|years?)\s+ago\b",
                  "", text, flags=re.IGNORECASE)

    # remove spaces before punctuation (. , ; : ! ?)
    text = re.sub(r"\s+([.,;!?])", r"\1", text)

    # remove multiplied spaces
    text = re.sub(r"\s{2,}", " ", text)

    # strip leading spaces
    return text.strip()
#--------------------------------

def ask_the_web(question):
    driver = webdriver.Firefox()

    # search query
    url = f"https://duckduckgo.com/?q={question}"
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    results = []
    snippets = []

    for article in soup.select("article[data-testid='result']"):
        # Get title and URL
        title_tag = article.select_one("a[data-testid='result-title-a']")
        title = title_tag.get_text(strip=True) if title_tag else None
        url_tag = article.select_one("a[data-testid='result-title-a']")
        url = url_tag["href"] if url_tag else None
        
        if title and url:
            results.append({"title": title, "url": url})

        # Snippets
        snippet_tag = article.select_one("[data-result='snippet']")
        snippet = snippet_strippet(snippet_tag) if snippet_tag else None
        snippets.append(snippet)

    combined_text = " ".join(snippets)
    driver.quit()
    return results, combined_text
#--------------------------------

# Temporary main
if __name__ == "__main__":
    web_finds = ask_the_web("what is the capital of france")

    for r in web_finds[:5]:
        print(r["title"])
        print(r["url"])
        print(r["snippet"])
        print("----")
#--------------------------------

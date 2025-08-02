#--------------------------------

# Imports
from selenium import webdriver
from bs4 import BeautifulSoup
#--------------------------------

driver = webdriver.Firefox()

# search query
query = "what is the capital of france"
url = f"https://duckduckgo.com/?q={query}"
driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
results = []

for article in soup.select("article[data-testid='result']"):
    # Title
    title_tag = article.select_one("a[data-testid='result-title-a']")
    title = title_tag.get_text(strip=True) if title_tag else None

    # URL
    url_tag = article.select_one("a[data-testid='result-title-a']")
    url = url_tag["href"] if url_tag else None

    # Snippet
    snippet_tag = article.select_one("[data-result='snippet']")
    snippet = snippet_tag.get_text(strip=True) if snippet_tag else None

    if title and url:
        results.append({"title": title, "url": url, "snippet": snippet})

# Print results
for r in results[:5]:
    print(r["title"])
    print(r["url"])
    print(r["snippet"])
    print("----")

driver.quit()
#--------------------------------

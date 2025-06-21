import requests
from bs4 import BeautifulSoup
import psycopg2
import time

BASE_URL = "https://theconversation.com/"
SEARCH_URL = "https://theconversation.com/topics/"
NUM_PAGES = 1

headers = {
    "User-Agent": "...Safari...",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}

def get_article_links(topic, page):
    # Extract article urls using given topic
    params = {"page": page}
    res = requests.get(SEARCH_URL + topic, params=params, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    anchors = soup.select("article h2 a")
    links = [BASE_URL + a["href"] for a in anchors if a.get("href")]
    return links

def extract_article(url):
    # Extract article
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.find("h1", class_="legacy entry-title instapaper_title") \
            .strong.get_text(strip=True).replace('\xa0', ' ')
        date = soup.find("div", class_="timestamps").time.get('datetime')
        paragraphs = soup.find("div", itemprop="articleBody").find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs).replace("\n", "")
        return {"title": title, "pubdate": date, "content": content, "url": url}
    except Exception as e:
        print(f"[Error] {url}: {e}")
        return None
    
if __name__ == '__main__':
    # Collect urls
    topic = "psychology-28"
    urls = []
    for page in range(1, NUM_PAGES + 1):
        print(f"Scraping page {page}...")
        urls += get_article_links(topic, page)
    # Extract content, pubdate, etc.
    articles = [extract_article(url) for url in urls]
    import pandas as pd 


    df = pd.DataFrame.from_records(articles[1:3], )
    print(df)
    # print(articles[0])
# def insert_article(article, conn):
#     with conn.cursor() as cur:
#         cur.execute("""
#             INSERT INTO dw_articles (title, content, date, url, raw_json)
#             VALUES (%s, %s, %s, %s, %s)
#             ON CONFLICT (url) DO NOTHING;
#         """, (
#             article["title"],
#             article["content"],
#             article["date"],
#             article["url"],
#             article  # raw_json stored as JSONB
#         ))
#     conn.commit()

# # Connect to PostgreSQL
# conn = psycopg2.connect(
#     host="localhost",
#     dbname="news_data",
#     user="postgres",
#     password="your_password"
# )

# # Scrape and insert
# for page in range(1, NUM_PAGES + 1):
#     print(f"Scraping page {page}...")
#     links = get_article_links(QUERY, page)
#     for link in links:
#         article = extract_article(link)
#         if article:
#             insert_article(article, conn)
#         time.sleep(1)  # Respectful delay

# conn.close()
# print("✅ Done scraping and storing.")

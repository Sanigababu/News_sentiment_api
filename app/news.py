import feedparser

def fetch_news(symbol: str):
    query = f"{symbol}+stock"
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries[:3]]


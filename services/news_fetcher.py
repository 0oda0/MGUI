# services/news_fetcher.py
import feedparser

class NewsFetcher:
    rss_feeds = {
        "Cyberpunk 2077": "https://www.cyberpunk.net/en/news/rss",
        "Elden Ring": "https://store.steampowered.com/feeds/news/app/1245620/",
        "Counter-Strike 2": "https://blog.counter-strike.net/index.php/feed/",
        "Valorant": "https://playvalorant.com/en-us/news/feed/",
        "GTA V": "https://www.rockstargames.com/news/rss",
        "Minecraft": "https://www.minecraft.net/en-us/feed",
    }

    @staticmethod
    def fetch_news(game_name: str):
        url = NewsFetcher.rss_feeds.get(game_name)
        if not url:
            return []
        try:
            feed = feedparser.parse(url)
            news_items = []
            for entry in feed.entries[:5]:
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "")
                })
            return news_items
        except Exception as e:
            print(f"Ошибка загрузки новостей: {e}")
            return []
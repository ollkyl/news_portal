import feedparser
from datetime import datetime, timezone


def get_latest_news(since: datetime):
    rss_feeds = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.npr.org/1001/rss.xml",
        "https://lenta.ru/rss/news",
        "https://www.vedomosti.ru/rss/news",
        "https://www.kommersant.ru/RSS/news.xml",
        "https://ria.ru/export/rss2/index.xml",
        "https://www.interfax.ru/rss.asp",
    ]

    all_news = []
    since_utc = since.astimezone(timezone.utc)
    newest_time = since_utc

    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                if hasattr(entry, "published_parsed"):
                    entry_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

                    if entry_date > since_utc:
                        title = entry.title[:100]
                        content = f"{entry.title}\n\nRead more: {entry.link}"
                        all_news.append((title, content, entry_date))

                        if entry_date > newest_time:
                            newest_time = entry_date

        except Exception:
            continue

    return [(title, content) for title, content, date in all_news], newest_time

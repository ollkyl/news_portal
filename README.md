# News Portal

## Возможности

- Автоматический парсинг новостей из RSS-лент
- WebSocket для реального времени — мгновенное обновление ленты на фронтенде
- Панель администратора для управления и добавления новостей
- Ручное и автоматическое добавление новостей


## Установка

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск (локально)

Запуск в режиме разработки:

```bash
uvicorn app.main:app --reload
```

Главная страница: `http://localhost:8000`
Панель администратора: `http://localhost:8000/admin`

## Docker

Сборка образа:

```bash
docker build -t news-portal .
```

Запуск контейнера:

```bash
docker run -p 8000:8000 news-portal
```



## Использование

- Главная страница — просмотр всех новостей
- Панель администратора — включение/выключение авто-обновления, ручное добавление новостей


## Список источников (app/parser.py)

```python
rss_feeds = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.npr.org/1001/rss.xml",
    "https://lenta.ru/rss/news",
    "https://www.vedomosti.ru/rss/news",
    "https://ria.ru/export/rss2/index.xml",
    "https://www.interfax.ru/rss.asp",
    # CNN
    "http://rss.cnn.com/rss/edition.rss",
    "http://rss.cnn.com/rss/edition_world.rss",
    "http://rss.cnn.com/rss/edition_us.rss",
    "http://rss.cnn.com/rss/money_latest.rss",
    # New York Times
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    # International News
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.france24.com/en/rss",
    "https://www.euronews.com/rss",
    # Additional English sources
    "https://feeds.foxnews.com/foxnews/latest",
    "https://abcnews.go.com/abcnews/topstories",
    "https://www.theguardian.com/international/rss",
    "https://time.com/feed/",
]
```

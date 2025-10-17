# News Portal

Простое веб-приложение для агрегации новостей с автоматическим обновлением через RSS.

## Функциональность

-  Автоматический парсинг новостей из RSS-лент
-  WebSocket для мгновенного обновления новостей
-  Панель администратора для управления
-  Ручное и автоматическое добавление новостей

## Установка и запуск

1. Установите зависимости:

pip install -r requirements.txt

Запустите приложение:

bash
uvicorn app.main:app --reload

# Сборка образа
docker build -t news-portal .

# Запуск контейнера
docker run -p 8000:8000 news-portal
```



Главная страница: http://localhost:8000
Панель администратора: http://localhost:8000/admin

## Использование
Главная страница: Просмотр всех новостей
Панель администратора:
Включение/выключение авто-обновления
Ручное добавление новостей
WebSocket: Подключение по /ws/news для получения новых новостей в реальном времени

FastAPI - веб-фреймворк
SQLite - база данных
SQLAlchemy - ORM
WebSocket - реальное время
Jinja2 - HTML шаблоны
RSS парсинг - агрегация новостей

Список источников(app/parser.py): 
```bash
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
        # # Additional English sources
        "https://feeds.foxnews.com/foxnews/latest",
        "https://abcnews.go.com/abcnews/topstories",
        "https://www.theguardian.com/international/rss",
        "https://time.com/feed/",
    ]
```
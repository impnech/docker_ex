
import os
import json
import time
import logging
logger = logging.getLogger("fetcher-logger")
# import asyncio
# import threading
# import time
# import io
# import httpx
import redis
import requests
# from contextlib import asynccontextmanager
# from fastapi import FastAPI



REDIS_HOST = os.getenv("REDIS_HOST", "localhost")


REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PORT = int(os.getenv("REDIS_PORT", 6380))

FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL_SECONDS", 15))
NEWS_URL = os.getenv("NEWS_API_URL", "https://newsapi.org/v2/top-headlines")
channel_name = os.getenv('CHANNEL_NAME', "news_channel")
API_KEY = os.getenv("NEWS_API_KEY", "4cc64a84e6174534b459d65a22ef6656")

#redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

params = {
    "country": "us",
    "apiKey": API_KEY
}

def send_to_redis():

    #TODO: use fastApi or Flask
    response = requests.get(NEWS_URL, params=params)
    response.raise_for_status()
    data = response.json()
    articles = data.get("articles", [])

    for article in articles:
        url = article.get('url')
        # todo: (not actually) use redis set, with expiration date, to avoid cluttering in and out
        news_item = {
            "title": article.get("title", ""),
            "content": article.get("body") or article.get("content") or article.get("description", ""),
            "source": article.get("source", {'name': 'no-source'}).get("name", "no-source-name"),
            "url": url
        }
        logging.debug(f"trying to publish {news_item}")
        redis_client.publish(channel_name, json.dumps(news_item))

    print(f"successfully published {len(articles)} articles to Redis.")
    pass


while True:
    send_to_redis()
    time.sleep(FETCH_INTERVAL)
    pass

import redis
import os
import json
import logging
import pymongo

logger = logging.getLogger("processor-logger")

# TODO from .env

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PORT = int(os.getenv("REDIS_PORT", 6380))

MONGO_HOST = os.getenv('MONGO_HOST','localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT',27017))

channel_name = os.getenv('CHANNEL_NAME', "news_channel")

keyword_list = os.getenv("WORDS_LIST", ["algorithm",
                                        "automation",
                                        "bandwidth",
                                        "blockchain",
                                        "cloud",
                                        "compiler",
                                        "cybersecurity",
                                        "database",
                                        "encryption",
                                        "firmware",
                                        "framework",
                                        "hardware",
                                        "infrastructure",
                                        "interface",
                                        "kernel",
                                        "metadata",
                                        "network",
                                        "open-source",
                                        "protocol",
                                        "repository",
                                        "server",
                                        "software",
                                        "telemetry",
                                        "virtualization",
                                        "technology",
                                        "batteries",
                                        "battery",
                                        "launch",
                                        "radio",
                                        "electric",
                                        "tech",
                                        "compute"
                                        ] +
                         [
"firework", "people",  "trump",
                         ]
                         )

if isinstance(keyword_list,str):
    keyword_list: list[str] = sum((w.split(',') for w in keyword_list.split()), [])


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
mongo_client = pymongo.MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = mongo_client["mydatabase"]
collection = db["articles"]

collection.drop()

def add(collection, dct):
    """
    adds if dct not already in collection
    :param collection:
    :param dct:
    :return: True if needed to add, False if didn't
    """
    if collection.find_one(dct):
        return False
    collection.insert_one(dct.copy())
    return True
def read_from_redis():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel_name)
    print(f"did read from redis, {channel_name}, listening")
    for msg in pubsub.listen():
        if not msg['type'] == "message":
            continue

        article: dict[str,str] = json.loads(msg["data"])
        title = article['title'] or ""

        for x in keyword_list:
            if title.lower().find(x) != -1:
                if add(collection,article):
                    print(f"saved a matching article (by title): found word '{x}' in {title = }")
                continue

        content = (article['content'] or "")
        for x in keyword_list:

            if content.lower().find(x) == -1: continue
            if add(collection,article):
                print(f"saved a matching article (By content): found word '{x}' in {content = }")


if __name__ == '__main__':
    print("ready to read from redis")
    try:
        read_from_redis()
    except Exception as e:
        print(f"something went wrong, maybe try using docker to run mongo ")
        raise e



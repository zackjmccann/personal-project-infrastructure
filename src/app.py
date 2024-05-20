import os
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))

def get_cache_hit_count():
    retries = 5

    while True:
        try:
            return cache.incr('hits')

        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc

            retries -= 1
            time.sleep(0.5)

@app.route('/')
def main():
    count = get_cache_hit_count()
    return f'Viewed {count} times.\n'

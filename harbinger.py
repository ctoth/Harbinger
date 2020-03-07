from sanic.log import logger
from sanic.response import file, json
from sanic import Blueprint, Sanic
from redis import Redis
import redis_collections
import newsloader



app = Sanic(__name__)

@app.route('/news')
def news(req):
    job = newsloader.job_queue.enqueue(newsloader.retrieve_articles)
    logger.info("Enqueued news job with ID", job.id)
    return json(list(newsloader.articles))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

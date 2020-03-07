from sanic.response import file, json
from sanic import Blueprint, Sanic
from redis import Redis
import redis_collections
import newsloader

newsloader.job_queue.enqueue(newsloader.retrieve_articles)


app = Sanic(__name__)

@app.route('/news')
def news(req):
    return json(newsloader.articles)
    
app.run(host="0.0.0.0", port=8080, debug=True)

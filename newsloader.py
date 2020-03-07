from newsapi import NewsApiClient
import newspaper
import rq
from redis import Redis
import redis_collections

REDIS_CONNECTION = Redis(host="redis")

articles = redis_collections.List(key="articles")

job_queue = rq.Queue(connection=REDIS_CONNECTION)

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

NEWSPAPER_CONFIG = newspaper    .Config()
NEWSPAPER_CONFIG.browser_user_agent = USER_AGENT

client = NewsApiClient(api_key='c1410091691a4b8b9a8e962bf461473b')


def retrieve_article_urls(sources="google-news"):
    everything = client.get_everything(sources=sources)
    return [i['url'] for i in everything['articles']]

def process_urls(urls):
    for url in urls:
        process_article(url)



def retrieve_articles():
    download_job = job_queue.enqueue(retrieve_article_urls)
    job_queue.enqueue(process_urls, depends_on=download_job)

def process_article(article_url):
    article = newspaper.Article(article_url, config=NEWSPAPER_CONFIG)
    article.download()
    article.parse()
    articles.push({
        'title': article.title,
        'authors': article.authors,
        'text': article.text,
        'url': article.url,
    }
    )



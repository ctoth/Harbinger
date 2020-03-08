import newspaper
from newsapi import NewsApiClient

from logging import getLogger
logger = getLogger("Newsloader")

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

NEWSPAPER_CONFIG = newspaper    .Config()
NEWSPAPER_CONFIG.browser_user_agent = USER_AGENT

client = NewsApiClient(api_key='c1410091691a4b8b9a8e962bf461473b')


def retrieve_article_urls(sources, language="en"):
    headlines = client.get_top_headlines(sources=sources, language=language)
    return [i['url'] for i in headlines['articles']]


def process_urls(urls):
    for url in urls:
        try:
            yield process_article(url)
        except Exception:
            yield


def retrieve_articles(sources="google-news"):
    logger.info("Retrieving most recent news articles...")
    urls = retrieve_article_urls(sources=sources)
    return process_urls(urls)


def process_article(article_url):
    article = newspaper.Article(article_url, keep_article_html=True, config=NEWSPAPER_CONFIG)
    article.download()
    article.parse()
    article.nlp()
    logger.info("Parsed article ", article.title)
    return article_to_dict(article)

def article_to_dict(article):
    return {
        'title': article.title,
        'authors': article.authors,
        'description': article.meta_description,
        'publish_date': article.publish_date,
        'tags': article.tags,
        'summary': article.summary,
        'text': article.text,
        'url': article.canonical_link,
        'article_html': article.article_html,
        'source_url': article.source_url,
        'keywords': article.keywords,
    }

def process_newspaper(url):
    source = newspaper.build(url, config=NEWSPAPER_CONFIG, keep_article_html=True, memoize_articles=False)
    source.download_articles()
    for article in source.articles:
        article.parse()
        article.nlp()
        yield article_to_dict(article)

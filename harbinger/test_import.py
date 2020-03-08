import models, newsloader
models.create_schema()

articles = newsloader.process_newspaper('https://nytimes.com')
for article_dict in articles:
    article = models.Article.get_or_none(url=article_dict['url'])
    if article is None:
        article = models.import_article(article_dict)
        print(article.title)
    
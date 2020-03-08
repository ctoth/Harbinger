import models, newsloader
models.create_schema()

articles = newsloader.retrieve_articles()
article_dict = next(articles)
article = models.import_article(article_dict)

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('app.db', pragmas=(
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),
    ('foreign_keys', 1))
)


class BaseModel(Model):
    class Meta:
        database = db


class Source(BaseModel):
    name = CharField(null=True)
    url = CharField(index=True, unique=True)


class Article(BaseModel):
    title = CharField(index=True)
    text = TextField()
    summary = TextField()
    description = TextField()
    article_html = TextField()
    url = CharField(unique=True, index=True)
    publish_date = DateTimeField(null=True)
    import_date = DateTimeField()
    source = ForeignKeyField(Source, related_name='articles')


class Author(BaseModel):
    name = CharField(index=True)


class Tag(BaseModel):
    text = CharField()


class Keyword(BaseModel):
    text = CharField()


class ArticleKeywords(BaseModel):
    article = ForeignKeyField(Article, related_name="keywords")
    keyword = ForeignKeyField(Keyword, related_name="articles")


class ArticleAuthors(BaseModel):
    article = ForeignKeyField(Article, related_name='authors')
    author = ForeignKeyField(Author, related_name='articles')


class ArticleTags(BaseModel):
    article = ForeignKeyField(Article, related_name="tags")
    tag = ForeignKeyField(Tag, related_name="articles")


def import_article(article_dict):
    authors = article_dict.pop('authors')
    author_models = [Author.get_or_create(name=i)[0] for i in authors]
    tags = article_dict.pop('tags')
    tag_models = [Tag.get_or_create(text=i)[0] for i in tags]
    keywords = article_dict.pop('keywords')
    keyword_models = [Keyword.get_or_create(text=i)[0] for i in keywords]
    import_date = datetime.datetime.now()
    source_url = article_dict.pop('source_url')
    source = Source.get_or_create(url=source_url)[0]
    source.save()
    new_model = Article(authors=author_models, tags=tag_models,
                        source=source, import_date=import_date, **article_dict)
    new_model.save()
    return new_model


def create_schema():
    db.create_tables([Author, Tag, Source,  Article,
                      ArticleAuthors, ArticleKeywords, ArticleTags, ])

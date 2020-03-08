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
    name = CharField(index=True, unique=True)
    url = CharField(index=True, unique=True)


class Article(BaseModel):
    title = CharField(index=True)
    text = TextField()
    summary = TextField()
    description = TextField()
    article_html = TextField()
    url = CharField(unique=True, index=True)
    publish_date = DateTimeField()
    import_date = DateTimeField()
    source = ForeignKeyField(Source, related_name='articles')


class Author(BaseModel):
    name = CharField(index=True)


class Tag(BaseModel):
    text = CharField()


class ArticleAuthors(BaseModel):
    article = ForeignKeyField(Article, related_name='authors')
    author = ForeignKeyField(Author, related_name='articles')


class ArticleTags(BaseModel):
    article = ForeignKeyField(Article)
    tag = ForeignKeyField(Tag)

def import_article(article_dict):
    authors = article_dict.pop('authors')
    author_models = [Author(name=i) for i in authors]
    tags = article_dict.pop('tags')
    tag_models = [Tag(i) for i in tags]
    new_model = Article(authors=author_models, tags=tag_models, import_date=datetime.datetime.now(), **article_dict)
    new_model.save()
    return new_model


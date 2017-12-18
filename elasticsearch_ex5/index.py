from elasticsearch import Elasticsearch
from sqlalchemy import func, create_engine
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer


def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    return sessionmaker(bind=engine)


db_session = init_db('sqlite:///chgk.db')()


es = Elasticsearch()

try:
    es.indices.create(index='chgk-index')
    i = 0
    for instance in db_session.query(Question).order_by(Question.id):
        i += 1
        es.index(index='chgk-index', doc_type='chgk', id=instance.id,
                 body={'question': instance.text, 'answer': instance.answer})

    print(i)
    print('Проиндексировано')
except Exception:
    print('Индекс уже существует')
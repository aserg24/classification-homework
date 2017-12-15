import lxml.html
import lxml.etree
import requests
from datetime import datetime
from tqdm import tqdm, tqdm_notebook
from sqlalchemy import func, create_engine
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.schema import Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    category = Column(Text, nullable=False)

    def __init__(self, body, category):
        self.body = body
        self.category = category


def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    return sessionmaker(bind=engine)


db_session = init_db('sqlite:///lenta.db')()


def followTheLink(link):
    url = 'https://www.lenta.ru' + link
    response = requests.get(url)
    return lxml.html.fromstring(response.text)


def processItem(tree):
    category = tree.xpath('//a[@class="b-header-inner__block"]/text()')[0]
    body = ' '.join(tree.xpath('//div[@itemprop="articleBody"]/p/text()')).replace(u'\xa0', u' ')
    return category, body


def loadNews():
    now = datetime.now()
    now_url = '/{}/{}/{}'.format(now.year, now.month, now.day)
    tree = followTheLink(now_url)  # начинаем с архива за сегодняшнее число
    date = []
    while '2014' not in date:  # переходим на предыдущее число, пока не встретим 2014
        date = tree.xpath('//div[@class="b-archive__header-rubric"]/h1/span/text()')[0].split()
        item_urles = tree.xpath('//section[@class="b-longgrid-column"]/div/div[2]/h3/a/@href')

        for url in item_urles:
            itemTree = followTheLink(url)
            category, body = processItem(itemTree)
            news = News(body, category)
            db_session.add(news)
        db_session.commit()
        next_page_url = tree.xpath('//a[@class="control_mini"]/@href')[0]
        followTheLink(next_page_url)

    # db_session.query(News).filter(News.category == '69-я параллель').delete()
    # db_session.query(News).filter(News.category == 'Мир').delete()
    #db_session.query(News).filter(News.category == 'Россия').delete()
    #db_session.commit()
    #здесь же удалила новости так, чтобы в каждой категории было примерно


loadNews()
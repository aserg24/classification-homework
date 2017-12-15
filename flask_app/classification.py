from sqlalchemy import func, create_engine
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.schema import Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from loading import init_db, News


db_session = init_db('sqlite:///lenta.db')()

categories = list()
for i, cat in enumerate(db_session.query(News.category).distinct()):
    categories.append(cat[0])

print(categories)

text_clf = Pipeline([('vectorizer', CountVectorizer(max_df=0.2, ngram_range=(1,2))),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(penalty='elasticnet'))])

text_clf = text_clf.fit([instance.body for instance in db_session.query(News).order_by(News.id)],
                        [categories.index(i.category) for i in db_session.query(News).order_by(News.id)])

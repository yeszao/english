from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text

from src.db.engine import Base, DbEngine


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    url = Column(String(300), nullable=False, unique=True, default='')
    publication = Column(String(10), nullable=False)
    title = Column(String(250), nullable=False, default='')
    tagged_title = Column(String(300), nullable=False, default='')
    content_html = Column(Text, nullable=False, default='')
    tagged_content_html = Column(Text, nullable=False, default='')
    vocabulary_count = Column(Integer, nullable=False, default=0)
    word_count = Column(Integer, nullable=False, default=0)
    sentences = Column(Text, nullable=False, default='')
    vocabulary = Column(Text, nullable=False, default='')


if __name__ == '__main__':
    Base.metadata.create_all(DbEngine)

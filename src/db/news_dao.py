from typing import List

from src.db.engine import DbSession
from src.db.entity import News


class NewsDao:
    @staticmethod
    def add_one(news: News):
        with DbSession() as session:
            session.add(news)
            session.commit()

    @staticmethod
    def get_latest(size: int = 2) -> List[News]:
        with DbSession() as session:
            return session.query(News).order_by(News.date.desc()).limit(size).all()

    @staticmethod
    def get_by_id(news_id: int) -> News:
        with DbSession() as session:
            return session.query(News).filter(News.id == news_id).first()

    @staticmethod
    def get_by_url(url: str) -> News:
        with DbSession() as session:
            return session.query(News).filter(News.url == url).first()

    @staticmethod
    def get_all_news(page: int, size: int) -> List[News]:
        with DbSession() as session:
            page = max(1, page)
            offset = (page - 1) * size
            return session.query(News).order_by(News.date.desc()).offset(offset).limit(size).all()

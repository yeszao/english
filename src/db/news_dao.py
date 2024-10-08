from typing import List

from src.db.engine import DbSession
from src.db.entity import News


class NewsDao:
    @staticmethod
    def add_one(news: News):
        with DbSession() as session:
            if session.query(News).filter(News.url == news.url).first():
                return

            session.add(news)
            session.commit()

    @staticmethod
    def get_latest(size: int = 2) -> List[News]:
        with DbSession() as session:
            return session.query(News).order_by(News.created_at.desc()).limit(size).all()

    @staticmethod
    def get_by_id(news_id: int) -> News:
        with DbSession() as session:
            return session.query(News).filter(News.id == news_id).first()

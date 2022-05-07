from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class Question(Base):
    """The model of questions for the quiz."""

    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

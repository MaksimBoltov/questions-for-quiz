from typing import Optional

from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.exceptions import UniqueViolationException


def get_question(db: Session, question_id: int) -> Optional[models.Question]:
    """Returns the question object from the database."""
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def create_question(db: Session, question: schemas.Question) -> models.Question:
    """Creates a question object in the database if there is no object with this id yet.
    Otherwise raise UniqueViolationException.
    """
    # If an object with the same id is already in the database, then raise an exception
    if get_question(db, question.id):
        raise UniqueViolationException
    new_question = models.Question(**question.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


def get_or_create_question(
    db: Session, question: schemas.Question
) -> tuple[models.Question, bool]:
    """Creates a question object in the database if there is no question with such id or
    returns an already existing object. Returns the object itself and True if the object was
    created and False if the object was already in the database.
    """
    question_from_db = get_question(db, question.id)
    if question_from_db:
        return question_from_db, False

    new_question = create_question(db, question)
    return new_question, True

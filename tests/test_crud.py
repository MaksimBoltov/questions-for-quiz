from datetime import datetime

import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import app.models as models
from app import crud
from app.exceptions import UniqueViolationException
from app.schemas import Question


@pytest.mark.parametrize(
    "question_id, question_text, answer, created_at",
    [(1, "question", "answer", datetime(2020, 1, 1))],
)
def test_create_question(
    db: Session, question_id: int, question_text: str, answer: str, created_at: datetime
) -> None:
    """Tests the creation of a new question in the database."""
    question_in = Question(
        id=question_id, question=question_text, answer=answer, created_at=created_at
    )
    question = crud.create_question(db, question=question_in)
    assert question
    assert jsonable_encoder(question) == jsonable_encoder(question_in)
    assert db.query(models.Question).count() == 1
    assert db.query(models.Question).first() == question


@pytest.mark.parametrize(
    "question_id, question_text, answer, created_at",
    [(1, "question", "answer", datetime(2020, 1, 1))],
)
def test_create_question_unique_violation_exception(
    db: Session, question_id: int, question_text: str, answer: str, created_at: datetime
) -> None:
    """Tests an error when trying to re-create a question with the same id."""
    question_in = Question(
        id=question_id, question=question_text, answer=answer, created_at=created_at
    )
    crud.create_question(db, question=question_in)
    with pytest.raises(UniqueViolationException):
        crud.create_question(db, question=question_in)


@pytest.mark.parametrize(
    "question_id, question_text, answer, created_at",
    [(1, "question", "answer", datetime(2020, 1, 1))],
)
def test_get_question(
    db: Session, question_id: int, question_text: str, answer: str, created_at: datetime
) -> None:
    """Tests getting a question on the id parameter from the database."""
    question_in = Question(
        id=question_id, question=question_text, answer=answer, created_at=created_at
    )
    question = crud.create_question(db, question=question_in)
    question_2 = crud.get_question(db, question_id=question.id)
    assert question_2
    assert question.id == question.id
    assert jsonable_encoder(question) == jsonable_encoder(question_2)


def test_get_nonexistent_question(db: Session) -> None:
    """Tests getting a question with a non-existent id from the database."""
    question_id = 1
    question = crud.get_question(db, question_id=question_id)
    assert question is None


@pytest.mark.parametrize(
    "question_id, question_text, answer, created_at",
    [(1, "question", "answer", datetime(2020, 1, 1))],
)
def test_get_or_create_question_object_already_exists(
    db: Session, question_id: int, question_text: str, answer: str, created_at: datetime
) -> None:
    """Tests the function 'get_or_create_question' when trying to add an existing object to the database."""
    question_in = Question(
        id=question_id, question=question_text, answer=answer, created_at=created_at
    )
    crud.create_question(db, question=question_in)
    question, is_exists = crud.get_or_create_question(db, question_in)
    assert question
    assert jsonable_encoder(question_in) == jsonable_encoder(question)
    assert not is_exists


@pytest.mark.parametrize(
    "question_id, question_text, answer, created_at",
    [(1, "question", "answer", datetime(2020, 1, 1))],
)
def test_get_or_create_question_new_question(
    db: Session, question_id: int, question_text: str, answer: str, created_at: datetime
) -> None:
    """Tests the function 'get_or_create_question' when trying to add a new object to the database."""
    question_in = Question(
        id=question_id, question=question_text, answer=answer, created_at=created_at
    )
    question, is_exists = crud.get_or_create_question(db, question_in)
    assert question
    assert jsonable_encoder(question_in) == jsonable_encoder(question)
    assert is_exists

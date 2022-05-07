from typing import Optional

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas

from .crud import get_or_create_question


def _get_questions_from_external_api(count: int) -> list:
    """Returns random questions (in the amount of 'count') from a third-party external api:
    https://jservice.io/api/random?count={count}
    """
    try:
        response = requests.get(f"https://jservice.io/api/random?count={count}")
    except requests.exceptions.ConnectionError as ex:
        raise HTTPException(
            status_code=409,
            detail={
                "msq": "Unable to connect to an external service",
                "type": "Connection error",
            },
        )

    return response.json()


def add_new_questions_to_db(
    db: Session, questions_count: int
) -> Optional[models.Question]:
    """Adds new questions to the database in the amount of 'questions_count' and returns the last one added.
    If 'question_count' is not positive, then None is returned.
    """
    if questions_count <= 0:
        return None

    added_questions_count = 0
    last_created_question = None
    while added_questions_count != questions_count:
        received_questions = _get_questions_from_external_api(
            questions_count - added_questions_count
        )
        for question in received_questions:
            added_question, is_created = get_or_create_question(
                db, schemas.Question(**question)
            )
            if is_created:
                last_created_question = added_question
                added_questions_count += 1

    return last_created_question

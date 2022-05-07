from fastapi import Body, Depends, FastAPI
from sqlalchemy.orm import Session

import app.schemas as schemas

from .database import get_db
from .services import add_new_questions_to_db

tags_metadata = [
    {
        "name": "questions",
        "description": "Operations with questions.",
    },
]

app = FastAPI(
    title="QuestionsQuiz",
    version="0.1",
    description="An application for getting questions to the quiz.\n"
    "You can get questions from an external service and add them to your database.",
)


@app.post("/questions", tags=["questions"])
def add_new_questions(
    questions_num: int = Body(..., ge=0, embed=True), db: Session = Depends(get_db)
):
    """Processes the addition of new questions (in the amount of 'questions_num') for the quiz to the database.
    Returns last added question.
    """
    if questions_num == 0:
        return {}
    last_added_question = add_new_questions_to_db(db, questions_num)

    return schemas.Question(
        id=last_added_question.id,
        question=last_added_question.question,
        answer=last_added_question.answer,
        created_at=last_added_question.created_at,
    )

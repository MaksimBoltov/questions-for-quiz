import json
from datetime import datetime
from unittest import mock

import pytest

from app.services import *
from app.services import _get_questions_from_external_api


@mock.patch("requests.get")
def test_get_questions_from_external_api(mock_get) -> None:
    """Testing the returned json data."""
    questions_return = [{"id": 1}, {"id": 2}]
    mock_get.return_value.json = mock.Mock(return_value=json.dumps(questions_return))
    return_value = _get_questions_from_external_api(1)
    assert return_value == json.dumps(questions_return)


@mock.patch("requests.get")
def test_get_questions_from_external_api_connection_error(mock_get) -> None:
    """Testing error during connections to external service."""
    mock_get.side_effect = requests.exceptions.ConnectionError()
    with pytest.raises(HTTPException):
        _get_questions_from_external_api(1)


@pytest.mark.parametrize("question_num", [-100, -1, 0])
def test_add_new_questions_to_db_question_count_le_0(
    db: Session, question_num: int
) -> None:
    """Tests getting questions when question_num lees or equal then 0."""
    assert add_new_questions_to_db(db, question_num) is None


@mock.patch("requests.get")
@pytest.mark.parametrize(
    "question_text, answer, created_at",
    [("question", "answer", "2020-01-01T01:01:01")],
)
def test_add_two_new_questions_to_db_and_get_last(
    mock_get, db: Session, question_text: str, answer: str, created_at: datetime
) -> None:
    """Tests adding questions to database and returning last of adding"""
    question_num = 2
    for_add = [
        {"id": i, "question": question_text, "answer": answer, "created_at": created_at}
        for i in range(1, question_num + 1)
    ]
    mock_get.return_value.json = mock.Mock(return_value=for_add)
    a = add_new_questions_to_db(db, question_num)
    assert a
    assert a.id == 2

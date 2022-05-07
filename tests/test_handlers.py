from unittest import mock

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_add_new_questions_handler_questions_num_lees_0(db_handlers):
    """Tries to add new questions to database with questions num lees then 0.
    Validations Error because questions_num can be more or equal then 0."""
    response = client.post("/questions", json={"questions_num": -1})
    print(response.json())
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "questions_num"],
                "msg": "ensure this value is greater than or equal to 0",
                "type": "value_error.number.not_ge",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_add_new_questions_handler_questions_num_equal_0(db_handlers):
    """"""
    response = client.post("/questions", json={"questions_num": 0})
    assert response.status_code == 200
    assert response.json() == {}


@mock.patch("requests.get")
def test_add_new_questions_handler_(mock_get, db_handlers):
    """Tests adding question to database and returning of last added question."""
    mock_get.return_value.json = mock.Mock(
        return_value=[
            {
                "id": 1,
                "question": "question",
                "answer": "answer",
                "created_at": "2020-01-01T01:01:01",
            }
        ]
    )
    response = client.post("/questions", json={"questions_num": 1})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "question": "question",
        "answer": "answer",
        "created_at": "2020-01-01T01:01:01",
    }

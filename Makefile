migrate:
	alembic revision --autogenerate -m 'Init'
	alembic upgrade head

runserver:
	uvicorn app.main:app --reload
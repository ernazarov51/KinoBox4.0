mig:
	alembic revision --autogenerate -m 'create table'
	alembic head alembic

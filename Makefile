.PHONY: run migration

run:
	python -m scheduler.main

migration:
	alembic upgrade head

run:
	uv run uvicorn page_analyzer:app --reload

lint:
	uv run ruff check
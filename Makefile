install:
	uv sync

run:
	uv run uvicorn page_analyzer:app --reload

lint:
	uv run ruff check

build:
	chmod +x ./build.sh
	./build.sh

PORT ?= 8000
render-start:
	uvicorn page_analyzer:app --host 0.0.0.0 --port $(PORT)
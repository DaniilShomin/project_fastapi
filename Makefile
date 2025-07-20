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
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
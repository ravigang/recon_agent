.PHONY: help install dev test lint format run run-cli docker-build docker-up clean

help:
	@echo "Available commands:"
	@echo "  make install       Install runtime dependencies"
	@echo "  make dev           Install all dependencies in editable mode with dev tools"
	@echo "  make test          Run pytest suite"
	@echo "  make lint          Run Ruff linter"
	@echo "  make run           Run Streamlit application"
	@echo "  make run-cli       Run reconciliation CLI on sample data"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-up     Start container via docker-compose"
	@echo "  make clean         Remove Python build/cache artifacts"

install:
	pip install .

dev:
	pip install -e ".[dev]"

test:
	pytest -v

lint:
	ruff check src tests scripts

format:
	ruff format src tests scripts

run:
	streamlit run src/recon_agent/presentation/streamlit/app.py

run-cli:
	python src/recon_agent/main.py

docker-build:
	docker build -t recon-agent:latest .

docker-up:
	docker-compose up --build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache dist build *.egg-info

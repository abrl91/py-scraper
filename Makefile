.PHONY: help install lint format type-check test clean run-dashboard

help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  lint         Run linting"
	@echo "  format       Run code formatting" 
	@echo "  type-check   Run type checking"
	@echo "  test         Run tests"
	@echo "  clean        Clean cache files"
	@echo "  run-dashboard Start Streamlit dashboard"

install:
	uv sync

lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests

type-check:
	uv run mypy src

test:
	uv run pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

run-dashboard:
	uv run streamlit run src/news_scraper/adapters/ui/dashboard.py
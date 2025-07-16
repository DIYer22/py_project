.PHONY: help install install-dev test lint format type-check clean build upload
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e .[dev]

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ --cov=py_project --cov-report=html --cov-report=term

lint: ## Run linting
	flake8 py_project tests

format: ## Format code with black and isort
	black py_project tests
	isort py_project tests

format-check: ## Check code formatting
	black --check py_project tests
	isort --check-only py_project tests

type-check: ## Run type checking
	mypy py_project

check: lint format-check type-check ## Run all checks

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## Build package
	python -m build

upload: build ## Upload package to PyPI
	python -m twine upload dist/*

upload-test: build ## Upload package to Test PyPI
	python -m twine upload --repository testpypi dist/*

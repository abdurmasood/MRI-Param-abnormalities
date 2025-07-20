.PHONY: help install install-dev test clean lint format type-check run-dashboard setup-db process-dicom

help:				## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:			## Install package dependencies
	pip install -r requirements.txt
	pip install -e .

install-dev:		## Install package with development dependencies
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:				## Run tests
	pytest tests/ -v

test-cov:			## Run tests with coverage
	pytest tests/ -v --cov=src/mri_param_analyzer --cov-report=html

clean:				## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

lint:				## Run linting
	flake8 src/ tests/ scripts/

format:				## Format code
	black src/ tests/ scripts/

type-check:			## Run type checking
	mypy src/

run-dashboard:		## Run the dashboard
	python -m mri_param_analyzer dashboard

setup-db:			## Setup database tables
	python -m mri_param_analyzer setup-db

process-dicom:		## Process DICOM files
	python -m mri_param_analyzer process-dicom

generate-test-data:	## Generate test DICOM data
	python scripts/generate_test_dicom.py

all-checks: lint type-check test		## Run all code quality checks 
# Makefile for Cleanup Toolkit Testing

.PHONY: help install test test-unit test-integration test-e2e test-all coverage clean lint format security performance

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
ISORT := $(PYTHON) -m isort
FLAKE8 := $(PYTHON) -m flake8
PYLINT := $(PYTHON) -m pylint
MYPY := $(PYTHON) -m mypy
BANDIT := $(PYTHON) -m bandit
COVERAGE := $(PYTHON) -m coverage

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Cleanup Toolkit - Test Suite$(NC)"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install test dependencies
	@echo "$(BLUE)Installing test dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-test.txt
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

test: ## Run all tests with coverage
	@echo "$(BLUE)Running all tests...$(NC)"
	$(PYTEST) tests/ -v --cov=. --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)Tests completed! Coverage report available in htmlcov/index.html$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	$(PYTEST) tests/unit/ -v -m unit --cov=. --cov-report=term

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	$(PYTEST) tests/integration/ -v -m integration --cov=. --cov-report=term

test-e2e: ## Run end-to-end tests only
	@echo "$(BLUE)Running end-to-end tests...$(NC)"
	$(PYTEST) tests/e2e/ -v -m e2e --cov=. --cov-report=term --timeout=300

test-performance: ## Run performance tests
	@echo "$(BLUE)Running performance tests...$(NC)"
	$(PYTEST) tests/performance/ -v -m performance --benchmark-only

test-security: ## Run security tests
	@echo "$(BLUE)Running security tests...$(NC)"
	$(PYTEST) tests/security/ -v -m security
	$(BANDIT) -r . -f json -o security-report.json || true
	@echo "$(GREEN)Security report saved to security-report.json$(NC)"

test-fast: ## Run fast tests only (exclude slow tests)
	@echo "$(BLUE)Running fast tests...$(NC)"
	$(PYTEST) tests/ -v -m "not slow" --cov=. --cov-report=term

test-all: ## Run all test types sequentially
	@echo "$(BLUE)Running complete test suite...$(NC)"
	$(MAKE) test-unit
	$(MAKE) test-integration
	$(MAKE) test-e2e
	$(MAKE) test-performance
	$(MAKE) test-security
	@echo "$(GREEN)All tests completed!$(NC)"

test-parallel: ## Run tests in parallel
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	$(PYTEST) tests/ -v -n auto --cov=. --cov-report=term

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Starting test watch mode...$(NC)"
	$(PYTEST) tests/ --watch

coverage: ## Generate coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	$(COVERAGE) run -m pytest tests/
	$(COVERAGE) report
	$(COVERAGE) html
	@echo "$(GREEN)Coverage report generated in htmlcov/index.html$(NC)"
	@echo "Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

coverage-xml: ## Generate XML coverage report for CI
	@echo "$(BLUE)Generating XML coverage report...$(NC)"
	$(COVERAGE) run -m pytest tests/
	$(COVERAGE) xml
	@echo "$(GREEN)XML coverage report saved to coverage.xml$(NC)"

lint: ## Run all linters
	@echo "$(BLUE)Running linters...$(NC)"
	@echo "Running Black..."
	$(BLACK) --check tests/ || true
	@echo "Running isort..."
	$(ISORT) --check-only tests/ || true
	@echo "Running Flake8..."
	$(FLAKE8) tests/ --count --statistics || true
	@echo "Running Pylint..."
	$(PYLINT) tests/ --exit-zero
	@echo "Running MyPy..."
	$(MYPY) tests/ --ignore-missing-imports || true
	@echo "$(GREEN)Linting completed!$(NC)"

format: ## Format code with Black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	$(BLACK) tests/
	$(ISORT) tests/
	@echo "$(GREEN)Code formatted successfully!$(NC)"

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	$(BANDIT) -r . -ll
	$(PYTHON) -m safety check --json > safety-report.json || true
	@echo "$(GREEN)Security checks completed!$(NC)"

clean: ## Clean test artifacts
	@echo "$(BLUE)Cleaning test artifacts...$(NC)"
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf coverage.json
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf junit/
	rm -rf benchmark*.json
	rm -rf security-report.json
	rm -rf safety-report.json
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)Cleanup completed!$(NC)"

shellcheck: ## Check shell scripts
	@echo "$(BLUE)Checking shell scripts...$(NC)"
	shellcheck hooks/pre-commit || true
	shellcheck scripts/*.sh || true
	shellcheck install.sh || true
	@echo "$(GREEN)Shell script check completed!$(NC)"

ci: ## Run CI pipeline locally
	@echo "$(BLUE)Running CI pipeline...$(NC)"
	$(MAKE) clean
	$(MAKE) install
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) security
	@echo "$(GREEN)CI pipeline completed successfully!$(NC)"

report: ## Generate test report
	@echo "$(BLUE)Generating test report...$(NC)"
	$(PYTEST) tests/ --html=test-report.html --self-contained-html
	@echo "$(GREEN)Test report saved to test-report.html$(NC)"

benchmark: ## Run benchmark tests
	@echo "$(BLUE)Running benchmarks...$(NC)"
	$(PYTEST) tests/performance/ --benchmark-only --benchmark-autosave
	@echo "$(GREEN)Benchmark results saved!$(NC)"

validate: ## Validate project setup
	@echo "$(BLUE)Validating project setup...$(NC)"
	@echo "Checking Python version..."
	$(PYTHON) --version
	@echo "Checking required files..."
	@test -f hooks/pre-commit && echo "✓ Pre-commit hook found" || echo "✗ Pre-commit hook missing"
	@test -f scripts/code_cleanup_gist.sh && echo "✓ Cleanup script found" || echo "✗ Cleanup script missing"
	@test -f requirements-test.txt && echo "✓ Test requirements found" || echo "✗ Test requirements missing"
	@test -f pyproject.toml && echo "✓ Project config found" || echo "✗ Project config missing"
	@echo "$(GREEN)Validation completed!$(NC)"

.DEFAULT_GOAL := help
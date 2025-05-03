.PHONY: lint
lint: ruff mypy	## Apply all the linters.

.PHONY: lint-check
lint-check:  ## Check whether the codebase satisfies the linter rules.
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@uv run ruff check $(path)
	@uv run mypy $(path)

.PHONY: ruff
ruff: ## Apply ruff.
	@echo "Applying ruff..."
	@echo "================"
	@echo
	@uv run ruff check --fix $(path)
	@uv run ruff format $(path)

.PHONY: mypy
mypy: ## Apply mypy.
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@uv run mypy $(path)


.PHONY: build-serve-docs
build-serve-docs: ## Build and serve the documentation.
	@echo
	@echo "Building and serving documentation..."
	@echo "==================================="
	@echo
	@uv run mkdocs serve

.PHONY: test-all
test-all: ## Run all tests in the test suite.
	@echo
	@echo "Running all tests..."
	@echo "==================="
	@echo
	@uv run pytest tests/

.PHONY: test-module
test-module: ## Run tests for a specific module. Usage: make test-module module=<module_path>
	@echo
	@echo "Running tests for module: $(module)"
	@echo "=================================="
	@echo
	@uv run pytest tests/$(module)
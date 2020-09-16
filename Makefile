# ImageMonk makefile

# You can set these variables from the command line
PROJECT = imagemonk

.PHONY: help
# Put it first so that "make" without argument is like "make help"
# Adapted from:
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## List Makefile targets
	$(info Makefile documentation)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'

tox: clean
	tox

clean-tox:
	rm -rf ./.mypy_cache
	rm -rf ./.tox
	rm -f .coverage
	find ./tests -type d -name __pycache__ -prune -exec rm -rf {} \;

clean-py:
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./*.egg-info
	find ./$(PROJECT) -type d -name __pycache__ -prune -exec rm -rf {} \;

clean-docs:
	rm -rf docs/_build
	rm -f docs/$(PROJECT)*.rst
	rm -f docs/modules.rst

clean: clean-tox clean-py clean-docs; ## Clean temp build/cache files and directories

wheel: ## Build Python binary distribution wheel package
	poetry build --format wheel

source: ## Build Python source distribution package
	poetry build --format sdist

test: ## Run the project testsuite(s)
	poetry run tox -r

docs: ## Build the documentation using Sphinx
	poetry run tox -e docs

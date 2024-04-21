.PHONY: install-dev start-local deploy help
.DEFAULT_GOAL := help
run-venv = python -m venv
run-uvicorn = python -m uvicorn
run-pulumi = pulumi

venv: # Create virtual environment
	$(run-venv) venv
	source venv/bin/activate

install-dev: # Install dev dependencies
	pip install -r requirements_dev.txt

start-local: # Start server in local
	$(run-uvicorn) app.server:app --reload

deploy: # Deploy to AWS
	$(run-pulumi) up

help: # make help
	@awk 'BEGIN {FS = ":.*#"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?#/ { printf "  \033[36m%-27s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

VERSION ?= $(shell git describe --tags --always --dirty --match=v* 2> /dev/null || echo "1.0.0")

.PHONY: default
default: help

# Read More https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## help information about make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install npm dependencies for the web service
	@echo "Installing Python dependencies"
	@python3 -m pip install -r requirements.txt

.PHONY: run
run: ## run the API server
	@echo "Starting API Server"
	@uvicorn app.main:app --reload


.PHONY: redis-start
redis-start: ## start the redis server
	@docker run --rm --name facial_ev_service_redis -d redis redis-server --appendonly yes

.PHONY: redis-stop
redis-stop: ## stop the redis server
	docker stop facial_ev_service_redis

.PHONY: version
version: ## display the version of the API server
	@echo $(VERSION)

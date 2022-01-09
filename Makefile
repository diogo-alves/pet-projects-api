TEST_TARGET=./tests
PACKAGE_MANAGER = poetry
RUNNER = ${PACKAGE_MANAGER} run


## @ Help
.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


## @ Dependencies
.PHONY: install
install: ## Install all project dependencies
	@ echo "Installing project dependencies..."
	${PACKAGE_MANAGER} install


## @ Utils
.PHONY: secret-key
secret-key: ## Generate a secret key for the SECRET_KEY environment variable
	${RUNNER} python manage.py utils gensecretkey
	@ echo '----------------------------------------------------------------'
	@ echo "Copy the generated secret key and paste it into your .env file"


## @ Local
.PHONY: local local-run local-migrations
local-run: ## Run app locally
	@ echo "Running webserver..."
	${RUNNER} uvicorn app.main:app --reload
local-migrations: ## Run database migrations locally
	@ echo "Running database migrations.."
	${RUNNER} alembic upgrade head
local: local-migrations local-run ## Run database migrations and app locally


## @ Docker
.PHONY: docker-up docker-migrations docker-down docker
docker-up: ## Create and start all services from docker-compose.yml
	@ echo "Starting docker services..."
	docker-compose up -d
docker-migrations: ## Run database migrations on database container
	@ echo "Running database migrations..."
	docker-compose exec web alembic upgrade head
docker-down: ## Stop and remove docker services resources
	@ echo "Stopping docker services..."
	docker-compose down
docker: docker-up docker-migrations ## Run app and database migrations with Docker


## @ Linters
.PHONY: lint
lint: ## Run linters
	@ echo "Running linters..."
	${RUNNER} pre-commit run --all-files


## @ Tests
.PHONY: tests coverage
tests: ## Run tests
	@ echo "Running tests..."
	${RUNNER} pytest ${TEST_TARGET}
coverage: ## Generate tests coverage report
	@ echo "Generating tests coverage report..."
	${RUNNER} pytest --cov=app --cov-report=html ${TEST_TARGET}


## @ Management commands
.PHONY: commands
commands: ## Show help for management commands
	@ echo "Showing help for managment commands..."
	@ ${RUNNER} python manage.py --help

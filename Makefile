.PHONY: help up down logs ps build rebuild clean init-db shell-backend shell-db scrape

# Default environment file
ENV_FILE ?= .env

up: ## Start all services in detached mode
	docker-compose --env-file $(ENV_FILE) up -d

down: ## Stop and remove all services, networks, and volumes
	docker-compose --env-file $(ENV_FILE) down -v --remove-orphans

logs: ## Tail logs for all services
	docker-compose --env-file $(ENV_FILE) logs -f

ps: ## List running services
	docker-compose --env-file $(ENV_FILE) ps

build: ## Build or rebuild services
	docker-compose --env-file $(ENV_FILE) build

rebuild: ## Rebuild services without cache
	docker-compose --env-file $(ENV_FILE) build --no-cache

clean: down ## Alias for down
	@echo "Project cleaned."

init-db: ## Initialize the database (create tables, load CSV data)
	@echo "Initializing database using app.db.init_db module..."
	docker-compose --env-file $(ENV_FILE) exec backend python -m app.db.init_db

shell-backend: ## Access a shell inside the backend container
	docker-compose --env-file $(ENV_FILE) exec backend bash

shell-db: ## Access psql shell in the postgres container
	docker-compose --env-file $(ENV_FILE) exec postgres psql -U $${POSTGRES_USER:-bacterial_user} -d $${POSTGRES_DB:-bacterial_classification}

scrape: ## Run the MimeDB scraper (example command)
	@echo "Running scraper with options: $(OPTS)"
	docker-compose --env-file $(ENV_FILE) exec scraper python -m src.main $(OPTS)

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

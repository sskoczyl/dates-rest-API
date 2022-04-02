PROJ_ROOT=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PYTHON_EXEC?=python
COMPOSE_EXEC?=docker-compose

PROD_DOCKER_COMPOSE=./docker-compose.yml
DEV_DOCKER_COMPOSE=./docker-compose.dev.yml

# RUN APP 
run-dev:
	$(COMPOSE_EXEC) -f $(DEV_DOCKER_COMPOSE) up $(filter-out $@,$(MAKECMDGOALS))

build:
	$(COMPOSE_EXEC) -f $(PROD_DOCKER_COMPOSE) build $(filter-out $@,$(MAKECMDGOALS))

build-dev:
	$(COMPOSE_EXEC) -f $(DEV_DOCKER_COMPOSE) build $(filter-out $@,$(MAKECMDGOALS))

migrate:
	$(COMPOSE_EXEC) exec api python manage.py migrate

# TEST AND LINT APP
test:
	$(COMPOSE_EXEC) -f $(DEV_DOCKER_COMPOSE) run --rm api pytest . -vv

lint:
	$(COMPOSE_EXEC) -f $(DEV_DOCKER_COMPOSE) run --rm api black .


# DEPENDENCIES
compile-deps:
	$(PYTHON_EXEC) -m piptools compile --no-annotate --no-header --generate-hashes "${PROJ_ROOT}/api/requirements/dev.in"
	$(PYTHON_EXEC) -m piptools compile --no-annotate --no-header --generate-hashes "${PROJ_ROOT}/api/requirements/prod.in"

recompile-deps:
	$(PYTHON_EXEC) -m piptools compile --no-annotate --no-header --generate-hashes --upgrade "${PROJ_ROOT}/api/requirements/dev.in"
	$(PYTHON_EXEC) -m piptools compile --no-annotate --no-header --generate-hashes --upgrade "${PROJ_ROOT}/api/requirements/prod.in"

sync-deps:
	$(PYTHON_EXEC) -m piptools help >/dev/null 2>&1 || $(PYTHON_EXEC) -m pip install pip-tools
	$(PYTHON_EXEC) -m piptools sync "${PROJ_ROOT}/api/requirements/dev.txt"

# Silent unused rules
%:
	@:

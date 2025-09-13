CURDIR := $(shell cd)

# Docker Desktop
docker_build_project:
	docker build -t twitch-bi .

docker_run_project:
	docker run --rm -it --env-file .env -v ${CURDIR}/data:/app/data twitch-bi

docker_run_project_full_refresh:
	docker run --rm -it --env-file .env -v ${CURDIR}/data:/app/data twitch-bi \
	dbt run --full-refresh --vars '{"export_all": true}'

# Docker Hub
docker_hub_push: docker_build_project
	docker tag twitch-bi gabriellegall/twitch-bi:latest
	docker push gabriellegall/twitch-bi:latest

docker_hub_pull_and_run:
	docker pull gabriellegall/twitch-bi:latest
	docker run --rm -it --env-file .env -v ${CURDIR}/data:/app/data gabriellegall/twitch-bi:latest

# DuckDB UI
duckdb_ui:
	duckdb -ui data/prod.duckdb
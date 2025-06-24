CURDIR := $(shell cd)

docker_build_project:
	docker build -t twitch-bi .

docker_run_project:
	docker run --rm -it -v ${CURDIR}/data:/app/data twitch-bi

docker_hub_push: docker_build_project
	docker tag twitch-bi gabriellegall/twitch-bi:latest
	docker push gabriellegall/twitch-bi:latest

docker_hub_pull_and_run:
	docker pull gabriellegall/twitch-bi:latest
	docker run --rm -it -v ${CURDIR}/data:/app/data gabriellegall/twitch-bi:latest

duckdb_ui:
	duckdb -ui data/prod.duckdb
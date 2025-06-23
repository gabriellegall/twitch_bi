CURDIR := $(shell cd)

docker_build_project:
	docker build -t twitch-bi .

docker_run_project:
	docker run --rm -it -v ${CURDIR}/data:/app/data twitch-bi

duckdb_ui:
	duckdb -ui data/prod.duckdb
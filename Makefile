CURDIR := $(shell cd)

docker_build_project:
	docker build -t twitch-bi .

docker_run_project:
	docker run -it -v ${CURDIR}/data:/app/data twitch-bi
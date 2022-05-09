NAME ?= lukewilson37
DOCKERNAME ?= mssa
IMAGENAME ?= mssa-flask
VERSION ?= 1
DOCKERFILE ?= dockerfile.api

test: py_test build run clean

init: build run gather

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

logs:
	docker logs "${DOCKERNAME}"

py_test:
	pytest

clean:
	docker stop "${DOCKERNAME}"
	docker rm "${DOCKERNAME}"

build:
	 docker build -t ${NAME}/${IMAGENAME}:${VERSION} -f ${DOCKERFILE} .

run:
	docker run --name "${DOCKERNAME}" -d -p 5037:5000 ${NAME}/${IMAGENAME}:${VERSION}

postdata:
	curl -X POST localhost:5037/data

getdata:
	curl localhost:5037/data

test:
	curl localhost:5037/

run_flask:
	 docker run --name "${NAME}-flask" -d -p 5037:5000 ${NAME}/whereisiss-flask:latest
	
push:
	docker push ${NAME}/${IMAGENAME}:${VERSION}

gather:
	curl -X POST localhost:5037/init

NAME ?= lukewilson37
DOCKERNAME ?= mssa
IMAGENAME ?= mssa-flask
VERSION ?= 1
DOCKERFILE ?= dockerfile.api

<<<<<<< HEAD
=======
upddock: build push

test: py_test build run clean

init: build run gather
>>>>>>> 974f8474743a7861a153fbca5d4bf5d175b30bdb

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


<<<<<<< HEAD
=======
test:
	curl localhost:5037/

run_flask:
	docker run --name "${NAME}-flask" -d -p 5037:5000 ${NAME}/whereisiss-flask:latest
>>>>>>> 974f8474743a7861a153fbca5d4bf5d175b30bdb
	

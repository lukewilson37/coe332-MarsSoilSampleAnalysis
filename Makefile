NAME ?= lukewilson37
DOCKERNAME ?= mssa
IMAGENAME ?= mssa-flask
VERSION ?= 1
DOCKERFILE ?= dockerfile.api


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


	

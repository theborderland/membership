NAME   := borderland.azurecr.io/pretix
TAG    := $$(git rev-parse HEAD)
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest
STABLE := ${NAME}:stable

build:
	docker build --no-cache --build-arg tag=${TAG} -t ${IMG} .
	docker tag ${IMG} ${LATEST}

stable:
	docker tag ${IMG} ${STABLE}
	docker push ${NAME}

push:
	docker push ${NAME}


NAME   := krav/pretix
TAG    := $$(git log -1 --pretty='%H')
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest
STABLE := ${NAME}:stable

build:
	docker build --build-arg tag=${TAG} -t ${IMG} .
	docker tag ${IMG} ${LATEST}

stable:
	docker tag ${IMG} ${STABLE}
	docker push ${NAME}
	aws ecs update-service --service pretix2 --force-new-deployment

push:
	docker push ${NAME}
	aws ecs update-service --service pretix2 --force-new-deployment


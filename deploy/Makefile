NAME   := krav/pretix
TAG    := $$(git log -1 --pretty='%H')
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest
STABLE := ${NAME}:stable

# pretix/standalone:stable 
build:
	docker build --build-arg tag=${TAG} -t ${IMG} .
	docker tag ${IMG} ${LATEST}

stable:
	docker tag ${IMG} ${STABLE}
	docker push ${NAME}

push:
	docker push ${NAME}


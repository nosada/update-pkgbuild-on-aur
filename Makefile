SHELL := /bin/bash

HOME_DIRECTORY=$(shell echo ${HOME})
REPOSITORY_LOCATION=$(shell pwd)
USER_SYSTEMD_LOCATION=${HOME_DIRECTORY}/.config/systemd/user

TEMPLATE=update-pkgbuild-on-aur.service.tmpl
NAME=update-pkgbuild-on-aur

FILES=bash \
	python \
	ssh_config \
	requirements.txt \
	Dockerfile \
	.dockerignore
DOCKER_IMAGE_NAME=local/${NAME}:latest

all: generate-systemd-service install activate-systemd-services

install: build-docker-image generate-systemd-service
	install -Dm 644 ${NAME}.service ${USER_SYSTEMD_LOCATION}
	install -Dm 644 ${NAME}.timer ${USER_SYSTEMD_LOCATION}

generate-systemd-service: ${TEMPLATE}
	sed -e 's;REPOSITORY_LOCATION;'${REPOSITORY_LOCATION}';g' ${TEMPLATE} > ${NAME}.service

build-docker-image: ${FILES}
	docker build . -t ${DOCKER_IMAGE_NAME}

activate-systemd-services:
	systemctl --user enable ${NAME}.service
	systemctl --user enable ${NAME}.timer
	systemctl --user start ${NAME}.timer
	systemctl --user daemon-reload

deactivate-systemd-services:
	systemctl --user disable ${NAME}.service
	systemctl --user disable ${NAME}.timer
	systemctl --user daemon-reload

clean: ${NAME}.service
	rm -f ${NAME}.service

uninstall: deactivate-systemd-services
	rm -f ${USER_SYSTEMD_LOCATION}/${NAME}.service
	rm -f ${USER_SYSTEMD_LOCATION}/${NAME}.timer
	docker rmi -f ${DOCKER_IMAGE_NAME}

SHELL := /bin/bash

HOME_DIRECTORY=$(shell echo ${HOME})
SCRIPT_LOCATION=$(shell pwd)
VENV_LOCATION=${HOME_DIRECTORY}/Venvs
USER_SYSTEMD_LOCATION=${HOME_DIRECTORY}/.config/systemd/user

FILES=update-pkgbuild-on-aur \
      update-pkgbuild-on-aur.service \
      update-pkgbuild-on-aur.timer \
      requirements.txt
TEMPLATE=update-pkgbuild-on-aur.service.tmpl
NAME=update-pkgbuild-on-aur

FILES_FOR_DOCKER=update-pkgbuild-on-aur \
		 requirements.txt \
		 Dockerfile \
		 .dockerignore
TEMPLATE_DOCKER=update-pkgbuild-on-aur.service.docker.tmpl
DOCKER_IMAGE_NAME=local/${NAME}:latest

all: generate-systemd-service install activate-systemd-services

install: build-docker-image generate-docker-systemd-service
	install -Dm 644 ${NAME}.service ${USER_SYSTEMD_LOCATION}
	install -Dm 644 ${NAME}.timer ${USER_SYSTEMD_LOCATION}

generate-systemd-service: ${TEMPLATE_DOCKER}
	sed -e 's|IMAGE_NAME|'${DOCKER_IMAGE_NAME}'|g' ${TEMPLATE_DOCKER} > ${NAME}.service

build-docker-image: ${FILES_FOR_DOCKER}
	docker build . -t ${DOCKER_IMAGE_NAME}

activate-systemd-services:
	systemctl --user enable ${NAME}.service
	systemctl --user enable ${NAME}.timer
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
	rm -rf ${VENV_LOCATION}/${NAME}

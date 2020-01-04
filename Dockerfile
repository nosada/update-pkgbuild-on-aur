FROM archlinux/base

ENV USER "builder"
ENV BASE_DIR "/pkgbuild"

ARG "GIT_USER_NAME"
ARG "GIT_USER_EMAIL"
ARG "AUR_SSH_PRIV_KEY"

RUN pacman -Syu pacman-contrib git python python-pip sudo \
	echo "$USER" ALL=(ALL) NOPASSWD > /etc/sudoers

WORKDIR $BASE_DIR
USER "$USER"

RUN mkdir -p "$BASE_DIR/.ssh/" \
	&& cat << EOF > "$BASE_DIR/.ssh/config"
Host aur.archlinux.org
	IdentityFile ~/.ssh/pribkey
	User aur
EOF \
	&& echo "$AUR_SSH_PRIV_KEY" > "$BASE_DIR/.ssh/pribkey" \
	&& git config --global user.email "$GIT_USER_EMAIL" \
	&& git config --global user.name "$GIT_USER_NAME"

COPY . .
RUN pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt

CMD ["python", "/app/python/entrypoint.py"]

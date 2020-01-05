# Install required package to archlinux/base
FROM archlinux/base as base
RUN pacman -Syu --noconfirm python python-pip \
	pacman-contrib sudo \
	git openssh \
	base-devel devtools

# Build application base image
FROM base as prepared

ENV USER "builder"
ENV BASE_DIR "/pkgbuild"
ENV HOME "$BASE_DIR"

RUN useradd -m -d "$BASE_DIR" "$USER" \
	&& echo "$USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR $BASE_DIR
USER "$USER"

COPY --chown="$USER" requirements.txt .
RUN pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt

# Build application image
FROM prepared

ARG "GIT_USER_NAME"
ARG "GIT_USER_EMAIL"
ARG "AUR_SSH_PRIV_KEY"

RUN mkdir -p "$BASE_DIR/.ssh/" \
	&& echo -e "$AUR_SSH_PRIV_KEY" > "$BASE_DIR/.ssh/pribkey" \
	&& chmod 600 "$BASE_DIR/.ssh/pribkey" \
	&& git config --global user.email "$GIT_USER_EMAIL" \
	&& git config --global user.name "$GIT_USER_NAME"

COPY --chown="$USER" bash/ ./bash/
COPY --chown="$USER" python/ ./python/
COPY --chown="$USER" ssh_config ./.ssh/config

RUN ssh-keyscan -H aur.archlinux.org >> "$BASE_DIR/.ssh/known_hosts"

CMD ["/pkgbuild/python/entrypoint.py"]

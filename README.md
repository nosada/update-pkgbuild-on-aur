# update-pkgbuild-on-aur
Update PKGBUILD registered to AUR when packages upstream updated.

This may be useful for PKGBUILD maintainers who maintain frequently-updating software.

# Prerequirements
- Arch User Repository (AUR) account
- SSH keypair
  - Public key must be added to your AUR account
- Slack App token

# How to use
1. Create AUR account at https://aur.archlinux.org/
2. Generate SSH keypair and add public key to AUR
3. Add your PKGBUILD to AUR
4. Add Slack App to your workspace
5. Invite your app to your workspace / channel
6. Generate Slack App token in https://api.slack.com
7. Set up `docker-compose.yaml` (See `docker-compose.yaml.tmpl` in detail)
8. `make`
9. That's all

# Usage
This expects to be used as Docker container and through `docker-compose`, but you can use `python/entrypoint.py` directly.

```
$ python/entrypoint.py -h
Update your PKGBUILD hosted in Arch User Repository (AUR) by your AUR account

Usage:
    entrypoint.py

Notes:
    Below environment variables must be set when calling this script:
        - MAINTAINER: AUR user name
        - SLACK_TOKEN: API token for Slack app
        - SLACK_CHANNEL: Name of Slack channel where you want to post update result
```

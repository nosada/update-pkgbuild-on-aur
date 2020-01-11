# update-pkgbuild-on-aur
Update PKGBUILD registered to AUR when packages upstream updated.

This may be useful for PKGBUILD maintainers who maintain frequently-updating software.

# Prerequirements
- Arch User Repository (AUR) account
- SSH keypair (public key must be added to your account in AUR)
- Slack incoming webhook URL

# How to use
1. Create AUR account at https://aur.archlinux.org/
2. Generate SSH keypair and add public key to AUR
3. Add your PKGBUILD to AUR
4. Generate Slack incoming webhook URL
4. Set up `docker-compose.yml` (See `docker-compose.yml.tmpl` in detail)
5. `make`
6. That's all

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
        - SLACK_WEBHOOK_URL: Webhook URL for Slack to notify update of
                             your package
```

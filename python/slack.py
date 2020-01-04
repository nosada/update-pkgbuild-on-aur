import slackweb


class SlackWebhook():
    def __init__(self, slack_webhook_url):
        self.slack = slackweb.Slack(url=slack_webhook_url)

    def post_package_upgraded(self, pkgname, pkgver,
                              returncode, stdout, stderr):
        if isinstance(stdout, bytes):
            stdout = stdout.decode()
        if isinstance(stderr, bytes):
            stderr = stderr.decode()

        if returncode != 0:
            result = ("Failed to build package with PKGBUILD of {p} {v}: "
                      "stdout={o}, stderr={e}").format(
                          p=pkgname, v=pkgver, o=stderr, e=stderr)
        else:
            result = "Package {p} is updated to version {v}".format(
                p=pkgname, v=pkgver
            )

        attachments = []
        attachment = {
            "pretext": "Package Update Result",
            "color": "warning",
            "fields": [
                {
                    "title": "Package Name",
                    "value": pkgname,
                    "short": False
                },
                {
                    "title": "Package Version in AUR",
                    "value": pkgver,
                    "short": True
                },
                {
                    "title": "Message",
                    "value": result,
                    "short": False
                },
            ]
        }
        attachments.append(attachment)
        self.slack.notify(attachments=attachments,
                          username="AUR package update",
                          icon_emoji=":mag:")

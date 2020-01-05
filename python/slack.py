import slackweb


class SlackWebhook():
    def __init__(self, slack_webhook_url):
        self.slack = slackweb.Slack(url=slack_webhook_url)
        self.message_template = """
{h}
*stdout*
```{o}```
*stderr*
```{e}```"""

    def post_package_upgraded(self, pkgname, pkgver,
                              returncode, stdout, stderr):
        if isinstance(stdout, bytes):
            stdout = stdout.decode()
        if isinstance(stderr, bytes):
            stderr = stderr.decode()

        if returncode != 0:
            header = "Failed to build package from PKGBUILD..."
        else:
            header = (
                "Succeeded to build package from PKGBUILD! "
                "New version will be pushed to AUR."
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
                }
            ]
        }
        attachments.append(attachment)
        self.slack.notify(attachments=attachments,
                          text=self.message_template.format(
                              h=header,
                              o=stdout,
                              e=stderr
                          ),
                          username="AUR package update",
                          icon_emoji=":up:")

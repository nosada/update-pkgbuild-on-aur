import slackweb


class Report():
    def __init__(self, slack_webhook_url):
        self.slack = slackweb.Slack(url=slack_webhook_url)
        self.message_template = """*stdout*
```{o}```
*stderr*
```{e}```"""

    def post_package_version_warning(self, pkgname, pkgver,
                                     upstream_version):
        attachments = []
        attachment = {
            "pretext": "Upstream version seems to be updated.",
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
                    "title": "Upstream Version",
                    "value": upstream_version,
                    "short": True
                },
            ]
        }
        attachments.append(attachment)
        self.slack.notify(attachments=attachments,
                          username="AUR package version checker",
                          icon_emoji=":mag:")

    def post_package_upgraded(self, pkgname, pkgver,
                              returncode, stdout, stderr):
        attachments = []
        attachment = {
            "pretext": "Result of Updating Package",
            "fields": [
                {
                    "title": "Package Name",
                    "value": pkgname,
                    "short": True
                },
                {
                    "title": "Package Version in AUR",
                    "value": pkgver,
                    "short": True
                },

            ]
        }

        if isinstance(stdout, bytes):
            stdout = stdout.decode()
        if isinstance(stderr, bytes):
            stderr = stderr.decode()

        result = {
            "title": "Result",
            "short": True
        }
        if returncode == 0:
            stderr = "Omitted"
            attachment["color"] = "good"
            result["value"] = "Succeeded"
        else:
            attachment["color"] = "danger"
            result["value"] = "Failed"
        attachment["fields"].append(result)

        attachments.append(attachment)
        self.slack.notify(attachments=attachments,
                          text=self.message_template.format(
                              o=stdout,
                              e=stderr
                          ),
                          username="AUR package update",
                          icon_emoji=":up:")

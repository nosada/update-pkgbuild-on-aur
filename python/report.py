from slack_sdk import WebClient


class Report():
    def __init__(self, slack_token, slack_channel):
        self.slack = WebClient(token=slack_token)
        self.channel = slack_channel

    def post_package_version_warning(self, pkgname, pkgver,
                                     upstream_version):
        attachments = []
        attachment = {
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

        text = "Upstream version seems to be updated."
        self.slack.chat_postMessage(channel=self.channel,
                                    text=text,
                                    attachments=attachments,
                                    username="AUR package version update",
                                    icon_emoji=":mag:")

    def post_package_upgraded(self, pkgname, pkgver,
                              returncode, stdout, stderr):
        attachments = []
        attachment = {
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

        if not stdout:
            stdout = "No messages"
        if not stderr:
            stderr = "No messages"

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

        # Report update result
        attachments.append(attachment)

        text = "Result of Updating Package"
        self.slack.chat_postMessage(channel=self.channel,
                                    text=text,
                                    attachments=attachments,
                                    username="AUR package update",
                                    icon_emoji=":up:")

        # Upload makepkg logs
        self.slack.files_upload_v2(channels=[self.channel],
                                content=stdout,
                                title="stdout",
                                initial_comment="Logs on stdout")
        self.slack.files_upload_v2(channels=[self.channel],
                                content=stderr,
                                title="stderr",
                                initial_comment="Logs on stderr")

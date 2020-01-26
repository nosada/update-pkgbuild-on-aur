#!/bin/env python

"""
Update your PKGBUILD hosted in Arch User Repository (AUR) by your AUR account

Usage:
    entrypoint.py

Notes:
    Below environment variables must be set when calling this script:
        - MAINTAINER: AUR user name
        - SLACK_WEBHOOK_URL: Webhook URL for Slack to notify update of
                             your package
"""

from docopt import docopt
import errno
import os
import sys

from out_of_date_pkgs import OutOfDateAURPackages
from pkgbuild import update_pkgbuild
from report import Report


if "MAINTAINER" not in os.environ:
    sys.stderr.write(
        "Enviromnet variable 'MAINTAINNER' must be set before running\n"
    )
    sys.exit(errno.ENOENT)

if "SLACK_WEBHOOK_URL" not in os.environ:
    sys.stderr.write(
        "Enviromnet variable 'SLACK_WEBHOOK_URL' must be set before running\n"
    )
    sys.exit(errno.ENOENT)


if __name__ == "__main__":
    docopt(__doc__)

    MAINTAINER = os.environ["MAINTAINER"]
    SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

    AUR = OutOfDateAURPackages(MAINTAINER)
    REPORT = Report(SLACK_WEBHOOK_URL)

    UPDATING = []
    for name, versions in AUR.get_out_of_date_packages():
        current_version = versions["package"]
        upstream_version = versions["upstream"]
        REPORT.post_package_version_warning(name, current_version,
                                            upstream_version)
        UPDATING.append(
            (name, upstream_version)
        )

    for name, upstream_version in UPDATING:
        returncode, stdout, stderr = update_pkgbuild(name, upstream_version)
        REPORT.post_package_upgraded(name, upstream_version,
                                     returncode, stdout, stderr)

import os
import subprocess


def update_pkgbuild(package_name, package_version):
    print("Update PKGBUILD of {p} to {v}".format(p=package_name,
                                                 v=package_version))

    where_am_i = os.path.dirname(os.path.realpath(__file__))

    result = subprocess.run(
        "/bin/bash {d}/../bash/update-pkgbuild {n} {v}".format(
            d=where_am_i,
            n=package_name, v=package_version).split(" "),
        capture_output=True,
        check=False
    )

    returncode = result.returncode
    stdout = result.stdout
    stderr = result.stderr

    return (returncode, stdout, stderr)

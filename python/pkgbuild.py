import subprocess


def update_pkgbuild(package_name, package_version):
    try:
        result = subprocess.run(
            "/bin/bash ../bash/update-pkgbuild {n} {v}".format(
                n=package_name, v=package_version).split(" "),
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as caught:
        returncode = -1
        stdout = None
        stderr = str(caught)

    returncode = result.returncode
    stdout = result.stdout
    stderr = result.stderr

    return (returncode, stdout, stderr)

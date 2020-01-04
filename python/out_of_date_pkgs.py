import re

import requests


class OutOfDateAURPackages():
    def __init__(self, maintainer):
        self.aur_endpoint = "https://aur.archlinux.org"
        self.maintainer = maintainer

        self.out_of_date_packages = {}

    def _get_maintained_packages(self):
        rpc_query = "/rpc/?v=5&type=search&by=maintainer&arg={m}".format(
            m=self.maintainer)
        response = requests.get(self.aur_endpoint + rpc_query).json()

        packages = response["results"]
        return packages

    def _get_upstream_url(self, package_name):
        rpc_query = "/rpc/?v=5&type=info&arg[]={p}".format(p=package_name)
        response = requests.get(self.aur_endpoint + rpc_query).json()

        info = response["results"]
        if info["URL"]:
            upstream = info["URL"]
        else:
            upstream = None
        return upstream

    def _get_latest_upstream_version(self, package_name):
        url = self._get_upstream_url(package_name)

        if not url:
            version = None
        else:
            # In case upstream is hosted in GitHub
            github_patterns = [
                r"^.*http[s]://github.com/([-_a-zA-Z0-9]*)/([-_a-zA-Z0-9]*)/*"
                r"^http[s]?://([-_a-zA-Z0-9]*).github.io/([-_a-zA-Z0-9]*)/*"
            ]
            for pattern in github_patterns:
                matched = re.match(pattern, url)
                if matched:
                    author, repo_name = matched.groups()
                    github_api_url = ("https://api.github.com/repos/"
                                      "{a}/{r}/releases/latest").format(
                                          a=author, r=repo_name)
                    version = requests.get(github_api_url).json()["tag_name"]

        return version

    @staticmethod
    def _is_latest_version(aur_pkg_version, upstream_version):
        """
        Comparation function. Current impletementation is too naive:
            AUR: 1.0.0, Upstream: 1.0.0 -> latest
            AUR: 1.0.0, Upstream: v1.0.1 -> NOT latest
            AUR: 1.1.0, Upstream: ver1.0.1 -> NOT latest (not occured...)
        """

        comparable_aur_pkg_version = aur_pkg_version.split("-")[0]
        return comparable_aur_pkg_version in upstream_version

    def get_out_of_date_packages(self):
        packages = self._get_maintained_packages()
        for package in packages:
            package_version = package["Version"]
            package_name = package["Name"]

            upstream_version = self._get_latest_upstream_version(package_name)

            if upstream_version:
                if not self._is_latest_version(package_version,
                                               upstream_version):
                    self.out_of_date_packages[package_name] = upstream_version
        return self.out_of_date_packages.items()

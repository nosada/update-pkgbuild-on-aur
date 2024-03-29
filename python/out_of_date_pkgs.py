from urllib.parse import quote
import re

from bs4 import BeautifulSoup
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
        rpc_query = "/rpc/?v=5&type=info&arg[]={p}".format(p=quote(package_name))
        response = requests.get(self.aur_endpoint + rpc_query).json()

        info = response["results"][0]
        if info["URL"]:
            upstream = info["URL"]
        else:
            upstream = None
        return upstream

    def _get_latest_upstream_version(self, package_name):
        url = self._get_upstream_url(package_name)
        version = None

        if url:
            # In case upstream is hosted in GitHub
            github_patterns = [
                r"^.*http[s]://github.com/([-_a-zA-Z0-9]*)/([-_a-zA-Z0-9]*)/*",
                r"^http[s]?://([-_a-zA-Z0-9]*).github.io/([-_a-zA-Z0-9]*)/*"
            ]
            for pattern in github_patterns:
                matched = re.match(pattern, url)
                if matched:
                    author, repo_name = matched.groups()
                    version = self._get_version_from_github(author, repo_name)

        if version:
            version_with_prefix = re.match(r"^v(er)?(\\.)?([.0-9]*)",
                                           version)
            if version_with_prefix:
                version = version_with_prefix.groups()[-1]
        return version

    @staticmethod
    def _get_version_from_github(author, repo_name):
        def _get(url, text=False):
            if text:
                return requests.get(url).text
            return requests.get(url).json()

        url = "https://api.github.com/repos/{a}/{r}/releases/latest".format(
            a=author, r=repo_name)

        version = None
        try:
            version = _get(url)["tag_name"]
        except KeyError:
            # OK, we'll use ugly and dirty scraping
            # Thanks to: https://stackoverflow.com/a/22735249
            url = "https://github.com/{a}/{r}/releases".format(
                a=author, r=repo_name)
            release_page = BeautifulSoup(_get(url, text=True), "html.parser")
            latest_release = release_page.find(
                lambda tag: tag.name == "div"
                and tag.get("class") == ["release-entry"])
            if latest_release:
                version = re.sub(r"[ \n]", "", latest_release.find("a").text)

        return version

    @staticmethod
    def _is_latest_version(aur_pkg_version, upstream_version):
        """
        Comparation function. Current impletementation is too naive:
            AUR: 1.0.0, Upstream: 1.0.0 -> latest
            AUR: 1.0.0, Upstream: 1.0.1 -> NOT latest
            AUR: 1.1.0, Upstream: 1.0.1 -> NOT latest (maybe not occured)
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
                if self._is_latest_version(package_version, upstream_version):
                    message = "{p} is up-to-date: {v}".format(
                        p=package_name, v=package_version
                    )
                else:
                    message = ("Version {u} is released in upstream of {p} "
                               "(current: {v})").format(p=package_name,
                                                        v=package_version,
                                                        u=upstream_version)
                    self.out_of_date_packages[package_name] = {
                        "upstream": upstream_version,
                        "package": package_version
                    }
            else:
                message = "Failed to get upstream version for {p}".format(
                    p=package_name
                )
            print(message)
        return self.out_of_date_packages.items()

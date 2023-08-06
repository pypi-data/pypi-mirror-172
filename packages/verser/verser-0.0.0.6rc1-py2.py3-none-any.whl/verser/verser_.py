import random
from .common.colors import *

# ------------------ CONFIGURATION --------------------------------------------
#


DEFAULT_START_VERSION = "0.0.0.0"
from dataclasses import dataclass
from pathlib import Path

from dataclasses import dataclass
from .common.files import Read, Write


@dataclass
class Project():
    package_name: str = "XYZ"
    default_version: str = DEFAULT_START_VERSION


test = False
mock_versions = {
    0: "1.0.17.2",
    1: "1.0.17.3rc2",
    2: "1.0.17.8rc6",
    3: "1.0.17.7",
    4: "1.0.17.9rc2",
    5: "1.0.17.9rc8",
}

import random


def mock_read(*args, **kwargs):
    x = random.choice(tuple(mock_versions.keys()))
    return mock_versions[x]


def increment_(next_status, prev_instance):
    major = prev_instance.major
    minor = prev_instance.minor
    patch = prev_instance.patch
    patch2 = prev_instance.patch2
    extra = prev_instance.extra
    if next_status and prev_instance.pre_release:
        # 1.3rc3<=#1.3rc2
        extra = extra + 1
    if next_status and not prev_instance.pre_release:
        # 1.4rc1<=#1.3
        patch2 = patch2 + 1
        extra = 1
    if not next_status and not prev_instance.pre_release:
        # 1.4<=#1.3
        patch2 = patch2 + 1
        extra = 0
    if not next_status and prev_instance.pre_release:
        # 1.3<=#1.3rc2
        patch2 = patch2 + 0
        extra = 0
    new_element = VersionParts(major, minor, patch, patch2, extra, next_status)

    return new_element


# ------------------------------------------- (Class) VersionParts
@dataclass
class VersionParts:
    major: int
    minor: int
    patch: int
    patch2: int
    extra: int = 0
    pre_release: bool = True
    version = ""

    def make_int(self, item):
        if isinstance(item, str):
            return int(item)
        return item

    def __post_init__(self):
        items = ("major", "minor", "patch", "patch2", "extra")
        for item in items:
            setattr(self, item, self.make_int(getattr(self, item)))

        self.combine()

    def combine(self):

        if self.pre_release:
            pre = "rc"
            self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}{pre}{self.extra}"
            return
        self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}"

    def __str__(self):
        return self.version


def create_version_instance(version: str):
    if not len(version.split(".")) > 3:
        print_with_failure_style(
            f"version : {version} does not fit to PEP. Continues with default start.{DEFAULT_START_VERSION}")
        version = DEFAULT_START_VERSION
    version = version.lower().replace("#", "").strip().replace("'", "")
    if "rc" in version:
        status_pre = True
        # 1.0.17.6rc2
        major, minor, patch, e = version.split(".")

        sp = e.split("rc")
        patch2 = int(sp[0])
        extra = int(sp[1])
    else:
        # 1.0.17.6
        status_pre = False
        major, minor, patch, patch2 = version.split(".")
        extra = 0
    instance = VersionParts(major, minor, patch, patch2, extra=extra, pre_release=status_pre)
    return instance


if test:
    Read = lambda x: mock_read(x)


class VersionNotFound(BaseException):
    """Version file not found """

    def __int__(self, *args):
        self.msg = f"Could find a proper version file, path may be given incorrectly path:  {', '.join(args)}"
        self.args = args

    def __str__(self):
        return self.msg


def get_previous(project):
    p = Path() / project.package_name / "__version__.py"
    if test:
        return Read(p)
    if p.is_file():
        c = Read(p)
        c = c.replace("version", "")
        c = c.replace("=", "").strip()
    else:
        raise VersionNotFound(p)
    return c


def get_prev_version_instance(project):
    try:
        previous_version = get_previous(project)
    except:
        previous_version = project.default_version
    return create_version_instance(previous_version)


# ---------------------------------------------------------------------
#               M A I N
# ---------------------------------------------------------------------
def get_next_version(project: Project = Project(),
                     increment=True,
                     pre_release=True,
                     verbose=True
                     ):
    """ M A I N   F U N C """
    prev_instance = get_prev_version_instance(project)

    if not increment:
        next_instance = prev_instance
    else:
        next_instance = increment_(pre_release, prev_instance)
    if verbose:
        print("-" * 15)
        print("CURRENT VERSION", prev_instance)
        print(f"increment_ : {increment}")
        print(f"pre_release : {pre_release}")
        print("NEW VERSION", next_instance)

    return next_instance


# ---------------------------------------------------------------------


__all__ = [
    'get_next_version',
    'Project'
]

"""
test_create_version_instance()
test_get_next_version()
pytest -v evdspy/EVDSlocal/scratches/verser.py
"""

#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of pygitsync.
#
#  You should have received a copy of the MIT License along with pygitsync.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import re
import typing

import pytest

from pygitsync._url import (
    SCP_STYLE_REGEX,
    URL_PREFIX_REGEX,
    GitUrlError,
    extract_git_project,
)

VALID_URLS = [
    "ssh://git@some.where/repo.git",
    "ssh://git@some.where/this_repo.git",
    "ssh://git@some.where/this-repo.git",
    "http://git@some.where/repo.git",
    "https://git@some.where/repo.git",
    "git://git@some.where/repo.git",
    "ftp://git@some.where/repo.git",
    "ftps://git@some.where/repo.git",
    "file:///some/where/repo.git",
]

VALID_SCP_PATHS = [
    "git@some.where:repo.git",
    "git@some.where:this_repo.git",
    "git@some.where:this-repo.git",
]

VALID_FILE_PATHS = [
    "this/is/the/local_project",
]


def check_valid_regex(pattern: str, under_test: typing.List[str]):
    success = []
    for this_item in under_test:
        if re.match(pattern, this_item):
            success.append(True)
        else:
            success.append(False)

    if not all(success):
        pytest.fail(str({a: b for a, b in zip(under_test, success)}))


def check_invalid_regex(pattern: str, under_test: typing.List[str]):
    failed = []
    for this_item in under_test:
        if not re.match(pattern, this_item):
            failed.append(True)
        else:
            failed.append(False)

    if not all(failed):
        pytest.fail(str({a: b for a, b in zip(under_test, failed)}))


class TestScpStyleRegex:
    def test_clean(self):
        check_valid_regex(SCP_STYLE_REGEX, VALID_SCP_PATHS)

    def test_invalid(self):
        # file:///some/where/repo.git is unfortunately a valid SCP path, so
        # have to take other action to ensure it is only processed as a URL.
        invalid_scp_paths = VALID_FILE_PATHS.copy() + [
            x for x in VALID_URLS if x != "file:///some/where/repo.git"
        ]
        check_invalid_regex(SCP_STYLE_REGEX, invalid_scp_paths)


class TestUrlPrefixRegex:
    def test_clean(self):
        check_valid_regex(URL_PREFIX_REGEX, VALID_URLS)

    def test_invalid(self):
        invalid_urls = [
            "git@some.where:repo.git",
            "git@some.where:this_repo.git",
            "this/is/the/local_project",
        ]
        assert not re.match(URL_PREFIX_REGEX, "git@some.where:repo.git")
        assert not re.match(URL_PREFIX_REGEX, "git@some.where:this_repo.git")
        assert not re.match(URL_PREFIX_REGEX, "this/is/the/local_project")


class TestExtractGitProject:
    def test_http_clean(self):
        result = extract_git_project(
            "http://some.where/this/is/the/http_project"
        )

        assert result == "http_project"

    def test_https_missing_repo(self):
        with pytest.raises(GitUrlError, match="^Incomplete git repository URL"):
            result = extract_git_project("https://some.where")

    def test_http_git_suffix_stripped(self):
        result = extract_git_project(
            "http://some.where/this/is/the/http_project.git"
        )

        assert result == "http_project"

    def test_scp_clean(self):
        result = extract_git_project("git@some.where:this/is/the/ssh_project")

        assert result == "ssh_project"

    def test_scp_missing_repo(self):
        # WARNING: even though this looks like an SCP path missing the repo
        # spec. it is technically a file path - an unusually name repo using "@"
        # and ".".
        result = extract_git_project("git@some.where")

        assert result == "git@some.where"

    def test_scp_git_suffix_stripped(self):
        result = extract_git_project(
            "git@some.where:this/is/the/ssh_project.git"
        )

        assert result == "ssh_project"

    def test_raw_path_clean(self):
        result = extract_git_project("this/is/the/local_project")

        assert result == "local_project"

    def test_raw_path_suffix_stripped(self):
        result = extract_git_project("this/is/the/local_project.git")

        assert result == "local_project"

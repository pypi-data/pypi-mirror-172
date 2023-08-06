#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of pygitsync.
#
#  You should have received a copy of the MIT License along with pygitsync.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""Git project URL management."""

import logging
import pathlib
import re
from urllib.parse import unquote, urlparse

from .exceptions import GitUrlError

log = logging.getLogger(__name__)

SCP_STYLE_REGEX = r"^([a-zA-Z0-9_\-]+@)?[0-9a-zA-Z_\-.]+:([\w/_\-]+(\.git)?)?$"
URL_PREFIX_REGEX = r"^((file)|(ftp(s)?)|(git)|(http(s)?)|(ssh))://"


def _extract_from_url(url: str) -> str:
    return (
        pathlib.PurePosixPath(unquote(urlparse(url).path))
        .parts[-1]
        .replace(".git", "")
    )


def _extract_from_raw_path(path: str) -> str:
    return pathlib.Path(path).parts[-1].replace(".git", "")


def _extract_from_scp_syntax(url: str) -> str:
    tokens = url.split(":")

    if len(tokens) != 2:
        raise IndexError(f"Incomplete git repository URL, {url}")

    return (
        pathlib.PurePosixPath(unquote(tokens[1])).parts[-1].replace(".git", "")
    )


def extract_git_project(url: str) -> str:
    """Extract git project name from a git repo URL.

    Args:
        url: Git repo URL to parse

    Returns:
        Git project name
    """
    try:
        if re.match(URL_PREFIX_REGEX, url.lower()):
            log.debug(f"extracting git project name from URL, {url}")
            value = _extract_from_url(url)
        elif re.match(SCP_STYLE_REGEX, url.lower()):
            log.debug(
                f"extracting git project name from SCP-style path-spec, {url}"
            )
            value = _extract_from_scp_syntax(url)
        else:
            log.debug(f"extracting git project name from raw path, {url}")
            value = _extract_from_raw_path(url)
    except IndexError as e:
        raise GitUrlError(f"Incomplete git repository URL, {url}") from e

    return value

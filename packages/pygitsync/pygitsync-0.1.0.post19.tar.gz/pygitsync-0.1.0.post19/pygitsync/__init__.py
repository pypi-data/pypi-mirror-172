#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of pygitsync.
#
#  You should have received a copy of the MIT License along with pygitsync.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""Periodically sync files from a remote git repository."""

from ._version import __version__  # noqa: F401
from .entrypoint import enter_fetch_run_loop  # noqa: F401

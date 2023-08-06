#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of pygitsync.
#
#  You should have received a copy of the MIT License along with pygitsync.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""``pygitsync`` exception declarations."""


class GitUrlError(Exception):
    """Problem occurred parsing git repository URL."""

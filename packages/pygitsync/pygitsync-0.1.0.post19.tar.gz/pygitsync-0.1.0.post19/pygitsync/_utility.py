#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of pygitsync.
#
#  You should have received a copy of the MIT License along with pygitsync.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""Miscellaneous utility classes and functions."""

import logging
import time
import types
import typing

log = logging.getLogger(__name__)

U = typing.TypeVar("U", bound="Timer")


class Timer:
    """A simple elapsed time context manager."""

    name: typing.Optional[str]
    start_time_seconds: float

    def __init__(self: U, name: typing.Optional[str] = None) -> None:
        """Construct ``Timer`` object."""
        self.name = name
        self.start_time_seconds = 0

    def __enter__(self: U) -> None:
        """Enter timer context."""
        if self.name:
            log.debug(f"starting timer for, {self.name}")
        else:
            log.debug("starting timer")

        self.start_time_seconds = time.time()

    def __exit__(
        self: U,
        context_type: typing.Optional[typing.Type[BaseException]],
        context_value: typing.Optional[BaseException],
        context_traceback: typing.Optional[types.TracebackType],
    ) -> None:
        """Exit timer context."""
        elapsed_time = time.strftime(
            "%H:%M:%S", time.gmtime(time.time() - self.start_time_seconds)
        )
        if self.name:
            log.info(f"{self.name} completed in, {elapsed_time}")
        else:
            log.info(f"elapsed, {elapsed_time}")

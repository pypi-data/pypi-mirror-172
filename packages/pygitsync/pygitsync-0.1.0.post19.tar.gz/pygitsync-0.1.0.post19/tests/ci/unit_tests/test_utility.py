#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of pygitsync.
#
#  You should have received a copy of the MIT License along with pygitsync.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import logging
import time

from pygitsync._utility import Timer


def test_no_label(caplog):
    with caplog.at_level(logging.INFO):
        with Timer():
            time.sleep(0.2)

    assert "elapsed, " in caplog.text
    assert "some label lapsed, " not in caplog.text


def test_label(caplog):
    with caplog.at_level(logging.INFO):
        with Timer("some label"):
            time.sleep(0.2)

    assert "elapsed, " not in caplog.text
    assert "some label completed in, " in caplog.text


def test_debug_start_no_label(caplog):
    with caplog.at_level(logging.DEBUG):
        with Timer():
            time.sleep(0.2)

    assert "starting timer" in caplog.text
    assert "starting timer for," not in caplog.text


def test_debug_start_label(caplog):
    with caplog.at_level(logging.DEBUG):
        with Timer("some label"):
            time.sleep(0.2)

    assert "starting timer for, some label" in caplog.text

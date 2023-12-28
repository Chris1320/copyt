#!/usr/bin/env python

"""
MIT License

Copyright (c) 2023 Chris1320

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os

from typer.testing import CliRunner

from copyt import info as copyt_info
from copyt._cli_handler import cmd

ENCODING = "utf-8"
CACHE_PATH = "./tests_data/copyt"
DB_FILE = os.path.join(CACHE_PATH, "history.db")

cmd_runner = CliRunner()


def cleanup_tests_data():
    """
    Cleanup the tests data
    """

    for path in os.listdir("./tests_data"):
        if path != ".gitinclude":
            os.remove(os.path.join("./tests_data", path))


def test_cli_version():
    """
    Test the version command
    """

    result = cmd_runner.invoke(cmd, ["version"])
    assert result.exit_code == 0
    assert (
        result.output
        == f"{copyt_info.NAME} v{'.'.join(map(str, copyt_info.VERSION))}\n"
    )


def test_cli_store_text_stdin():
    """
    Store text via stdin
    """

    test_data = "The quick brown fox jumps over the lazy dog."

    cleanup_tests_data()
    result = cmd_runner.invoke(
        cmd, ["--cache-path", CACHE_PATH, "store"], input=test_data
    )
    assert result.exit_code == 0
    with open(DB_FILE, "r", encoding=ENCODING) as f:
        assert f.read() == test_data

    cleanup_tests_data()


def test_cli_store_text_arg():
    """
    Store text via argument
    """

    test_data = "Another quick brown fox jumps over the lazy dog."

    cleanup_tests_data()
    result = cmd_runner.invoke(cmd, ["--cache-path", CACHE_PATH, "store", test_data])
    assert result.exit_code == 0
    with open(DB_FILE, "r", encoding=ENCODING) as f:
        assert f.read() == test_data

    cleanup_tests_data()

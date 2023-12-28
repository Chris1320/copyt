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

from typer.testing import CliRunner

from copyt import info as copyt_info
from copyt._cli_handler import cmd

cmd_runner = CliRunner()


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


def test_cli_store_stdin():
    """
    Store text via stdin
    """

    result = cmd_runner.invoke(
        cmd, ["--cache-path", "./tests_data/copyt", "store"], input="foo"
    )
    assert result.exit_code == 0


def test_cli_store_arg():
    """
    Store text via argument
    """

    result = cmd_runner.invoke(
        cmd, ["--cache-path", "./tests_data/copyt", "store", "foo"]
    )
    assert result.exit_code == 0

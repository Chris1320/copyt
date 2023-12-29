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
import pickle
import shutil
import sqlite3

from typer.testing import CliRunner

from copyt import info as copyt_info
from copyt._cli_handler import cmd

ENCODING = "utf-8"
CACHE_PATH = "./tests_data/copyt"
DB_FILE = os.path.join(CACHE_PATH, "history.db")

IMAGE_FILES = [
    "./tests_data/assets/pomeranian-pup.jpg",
    "./tests_data/assets/cat-1369563348jT2.jpg",
    "./tests_data/assets/lighted-match.jpg",
]

cmd_runner = CliRunner()


def cleanup_tests_data():
    """
    Cleanup the tests data
    """

    for path in os.listdir("./tests_data"):
        if path not in (".gitinclude", "assets"):
            shutil.rmtree(os.path.join("./tests_data", path))


def encode(data):
    """
    How sqlitedict encodes data
    """

    return sqlite3.Binary(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))


def decode(data):
    """
    How sqlitedict decodes data
    """

    return pickle.loads(bytes(data))


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


def test_cli_store_empty():
    """
    Attempt to call `store` command without any arguments or data from stdin
    """

    cleanup_tests_data()

    result = cmd_runner.invoke(cmd, ["--cache-path", CACHE_PATH, "store"])
    assert result.exit_code == 10
    assert result.output == "Nothing to store\n"
    cleanup_tests_data()


def test_cli_store_text_arg():
    """
    Store text via argument
    """

    test_data = "Another quick brown fox jumps over the lazy dog."

    cleanup_tests_data()
    result = cmd_runner.invoke(cmd, ["--cache-path", CACHE_PATH, "store", test_data])
    assert result.exit_code == 0
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        result = cur.execute(
            "SELECT value FROM clipboard WHERE key = ?", ("1",)
        ).fetchone()

        assert decode(result[0])["data"] == test_data

    cleanup_tests_data()


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
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        result = cur.execute(
            "SELECT value FROM clipboard WHERE key = ?", ("1",)
        ).fetchone()

        # STDIN is encoded as bytes since we can pipe binary data to it.
        assert decode(result[0])["data"].decode(ENCODING) == test_data

    cleanup_tests_data()


def test_cli_store_image_stdin():
    """
    Store an image via stdin
    """

    with open(IMAGE_FILES[0], "rb") as f:
        test_data = f.read()

    cleanup_tests_data()
    result = cmd_runner.invoke(
        cmd, ["--cache-path", CACHE_PATH, "store"], input=test_data
    )
    assert result.exit_code == 0
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        result = cur.execute(
            "SELECT value FROM clipboard WHERE key = ?", ("1",)
        ).fetchone()

        assert decode(result[0])["data"] == test_data

    cleanup_tests_data()


def test_cli_store_multi_text_stdin():
    """
    Store multiple texts via stdin
    """

    test_data = ["foo", "bar", "baz", "bat", "cat", "mat", "sat", "rat", "pat", "hack"]

    cleanup_tests_data()
    for data in test_data:
        cmd_result = cmd_runner.invoke(
            cmd, ["--cache-path", CACHE_PATH, "store"], input=data
        )
        assert cmd_result.exit_code == 0

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        db_result = cur.execute("SELECT * FROM clipboard").fetchall()

    assert len(db_result) == len(test_data)
    for idx, db_result in enumerate(db_result):
        # checked in the order they were added
        assert decode(db_result[1])["data"].decode(ENCODING) == test_data[idx]

    cleanup_tests_data()


def test_cli_store_multi_image_stdin():
    """
    Store multiple image files via stdin
    """

    cleanup_tests_data()
    for data in IMAGE_FILES:
        with open(data, "rb") as f:
            cmd_result = cmd_runner.invoke(
                cmd, ["--cache-path", CACHE_PATH, "store"], input=f.read()
            )
            assert cmd_result.exit_code == 0

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        db_result = cur.execute("SELECT * FROM clipboard").fetchall()

    assert len(db_result) == len(IMAGE_FILES)
    for idx, db_result in enumerate(db_result):
        # checked in the order they were added
        with open(IMAGE_FILES[idx], "rb") as f:
            assert decode(db_result[1])["data"] == f.read()

    cleanup_tests_data()

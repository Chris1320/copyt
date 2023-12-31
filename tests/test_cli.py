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

import json
import os
import pickle
import shutil
import sqlite3
from typing import Any

from typer.testing import CliRunner

from copyt import info as copyt_info
from copyt._cli_handler import cmd

ENCODING = "utf-8"
CACHE_PATH = "./tests_data/copyt"
DB_FILE = os.path.join(CACHE_PATH, "history.db")

TEST_TEXTS = ["foo", "bar", "baz", "bat", "cat", "mat", "sat", "rat", "pat", "hack"]
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


def encode(data: Any):
    """
    How sqlitedict encodes data
    """

    return sqlite3.Binary(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))


def decode(data: Any):
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

    result = cmd_runner.invoke(cmd, ["--cache-dir", CACHE_PATH, "store"])
    assert result.exit_code == 10
    assert result.output == "Nothing to store\n"
    cleanup_tests_data()


def test_cli_store_text_arg():
    """
    Store text via argument
    """

    test_data = "Another quick brown fox jumps over the lazy dog."

    cleanup_tests_data()
    result = cmd_runner.invoke(cmd, ["--cache-dir", CACHE_PATH, "store", test_data])
    assert result.exit_code == 0
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        result = cur.execute(
            "SELECT value FROM clipboard WHERE key = ?", ("1",)
        ).fetchone()

        assert decode(result[0]).content == test_data

    cleanup_tests_data()


def test_cli_store_text_stdin():
    """
    Store text via stdin
    """

    test_data = "The quick brown fox jumps over the lazy dog."

    cleanup_tests_data()
    result = cmd_runner.invoke(
        cmd, ["--cache-dir", CACHE_PATH, "store"], input=test_data
    )
    assert result.exit_code == 0
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        result = cur.execute(
            "SELECT value FROM clipboard WHERE key = ?", ("1",)
        ).fetchone()

        assert decode(result[0]).content == test_data

    cleanup_tests_data()


def test_cli_store_image_stdin():
    """
    Store an image via stdin
    """

    with open(IMAGE_FILES[0], "rb") as f:
        test_data = f.read()

    cleanup_tests_data()
    result = cmd_runner.invoke(
        cmd, ["--cache-dir", CACHE_PATH, "store"], input=test_data
    )
    assert result.exit_code == 0
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        result = cur.execute(
            "SELECT value FROM clipboard WHERE key = ?", ("1",)
        ).fetchone()

        assert decode(result[0]).content == test_data

    cleanup_tests_data()


def test_cli_store_multi_text_stdin():
    """
    Store multiple texts via stdin
    """

    cleanup_tests_data()
    for data in TEST_TEXTS:
        cmd_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "store"], input=data
        )
        assert cmd_result.exit_code == 0

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        db_result = cur.execute("SELECT * FROM clipboard").fetchall()

    assert len(db_result) == len(TEST_TEXTS)
    for idx, db_result in enumerate(db_result):
        # checked in the order they were added
        assert decode(db_result[1]).content == TEST_TEXTS[idx]

    cleanup_tests_data()


def test_cli_store_multi_image_stdin():
    """
    Store multiple image files via stdin
    """

    cleanup_tests_data()
    for data in IMAGE_FILES:
        with open(data, "rb") as f:
            cmd_result = cmd_runner.invoke(
                cmd, ["--cache-dir", CACHE_PATH, "store"], input=f.read()
            )
            assert cmd_result.exit_code == 0

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        db_result = cur.execute("SELECT * FROM clipboard").fetchall()

    assert len(db_result) == len(IMAGE_FILES)
    for idx, db_result in enumerate(db_result):
        # checked in the order they were added
        with open(IMAGE_FILES[idx], "rb") as f:
            assert decode(db_result[1]).content == f.read()

    cleanup_tests_data()


def test_cli_list_text_arg():
    """
    List command with data from argument
    """

    cleanup_tests_data()
    for data in TEST_TEXTS:
        cmd_txt_input_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "store", data]
        )
        assert cmd_txt_input_result.exit_code == 0

    cmd_result = cmd_runner.invoke(cmd, ["--cache-dir", CACHE_PATH, "list"])

    expected_output = ""
    for idx, data in enumerate(TEST_TEXTS):
        expected_output += f"{idx + 1}\t{data}\n"

    assert cmd_result.exit_code == 0
    assert cmd_result.output == expected_output

    cleanup_tests_data()


def test_cli_get_text_arg():
    """
    Get a text from the database via argument
    """

    cleanup_tests_data()

    # add test data
    for data in TEST_TEXTS:
        cmd_txt_input_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "store", data]
        )
        assert cmd_txt_input_result.exit_code == 0

    # get test data
    for idx, test_data in enumerate(TEST_TEXTS):
        cmd_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "get", str(idx + 1)]
        )

        assert cmd_result.exit_code == 0
        assert cmd_result.output == test_data

    cleanup_tests_data()


def test_cli_get_text_stdin():
    """
    Get a text from the database via stdin
    """

    cleanup_tests_data()

    # add test data
    for data in TEST_TEXTS:
        cmd_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "store"], input=data
        )
        assert cmd_result.exit_code == 0

    # get test data
    for idx, test_data in enumerate(TEST_TEXTS):
        cmd_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "get"], input=str(idx + 1)
        )
        assert cmd_result.exit_code == 0
        assert cmd_result.output == test_data

    cleanup_tests_data()


def test_cli_delete_text_arg():
    """
    Remove a text from the database via arguments
    """

    td = ("foo", "bar", "baz")

    cleanup_tests_data()

    # add test data
    for data in td:
        cmd_store_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "store"], input=data
        )
        assert cmd_store_result.exit_code == 0

    # delete test data
    cmd_delete_result = cmd_runner.invoke(
        cmd, ["--cache-dir", CACHE_PATH, "delete", "2"]
    )
    assert cmd_delete_result.exit_code == 0

    # get remaining test data
    cmd_result = cmd_runner.invoke(cmd, ["--cache-dir", CACHE_PATH, "list"])

    assert cmd_result.exit_code == 0
    assert cmd_result.output == "1\tfoo\n3\tbaz\n"

    cleanup_tests_data()


def test_cli_delete_text_stdin():
    """
    Remove a text from the database via stdin
    """

    td = ("foo", "bar", "baz")

    cleanup_tests_data()

    # add test data
    for data in td:
        cmd_store_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "store"], input=data
        )
        assert cmd_store_result.exit_code == 0

    # delete test data
    cmd_delete_result = cmd_runner.invoke(
        cmd, ["--cache-dir", CACHE_PATH, "delete"], input="2"
    )
    assert cmd_delete_result.exit_code == 0

    # get remaining test data
    cmd_result = cmd_runner.invoke(cmd, ["--cache-dir", CACHE_PATH, "list"])

    assert cmd_result.exit_code == 0
    assert cmd_result.output == "1\tfoo\n3\tbaz\n"

    cleanup_tests_data()


def test_cli_version_json():
    """
    Test the version command with json output
    """

    result = cmd_runner.invoke(cmd, ["--json", "version"])
    assert result.exit_code == 0
    assert (
        result.output
        == json.dumps({"name": copyt_info.NAME, "version": copyt_info.VERSION}) + "\n"
    )


def test_cli_store_empty_json():
    """
    Attempt to call `store` command without any
    arguments or data from stdin with json output
    """

    cleanup_tests_data()

    result = cmd_runner.invoke(cmd, ["--cache-dir", CACHE_PATH, "--json", "store"])
    assert result.exit_code == 10
    assert result.output == json.dumps({"error": "Nothing to store"}) + "\n"
    cleanup_tests_data()


def test_cli_list_text_arg_json():
    """
    List command with data from argument with json output
    """

    cleanup_tests_data()
    for data in TEST_TEXTS:
        cmd_txt_input_result = cmd_runner.invoke(
            cmd, ["--cache-dir", CACHE_PATH, "--json", "store", data]
        )
        assert cmd_txt_input_result.exit_code == 0

    cmd_result = cmd_runner.invoke(cmd, ["--cache-dir", CACHE_PATH, "--json", "list"])
    assert cmd_result.exit_code == 0

    for idx, data in enumerate(json.loads(cmd_result.output)):
        assert str(idx + 1) == data[0]
        assert TEST_TEXTS[idx] == data[1]["content"]

    cleanup_tests_data()

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
from typing import Any

from typer.testing import CliRunner

from copyt.api import API
from copyt.models.global_options import GlobalOptions

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


def test_max_items():
    """
    Test how the "max items" feature works
    """

    cleanup_tests_data()
    copyt_api = API(
        GlobalOptions(
            json=False,
            max_items=1000,
            max_item_size_in_bytes=512,
            verbose=False,
            cache_dir=CACHE_PATH,
            text_encoding=ENCODING,
        )
    )

    for idx in range(1, 1101):
        copyt_api.store(f"test #{idx}")

    copyt_api.commit()

    for idx in range(1, 101):
        try:
            assert copyt_api.get_record_from_id(idx) is None

        except KeyError:
            pass

        else:
            raise AssertionError(f"Record #{idx} was not deleted")

    for idx in range(101, 1101):
        assert copyt_api.get_record_from_id(idx) is not None

    cleanup_tests_data()

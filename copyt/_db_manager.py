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
import pathlib

from sqlitedict import SqliteDict


class DBManager:
    """
    This class handles all interactions with the database.
    """

    def __init__(
        self,
        db_path: pathlib.Path,
        target: str = "clipboard",
        encoding: str = "utf-8",
    ):
        self._db_path = db_path
        self._target = target
        self.encoding = encoding

        os.makedirs(self._db_path.parent, exist_ok=True)
        self._db = SqliteDict(
            self._db_path, tablename=self._target, journal_mode="OFF", outer_stack=False
        )

    @property
    def max_index(self) -> int:
        """
        Get the maximum index in the database.
        """

        if len(tuple(self._db.keys())) > 0:
            return max(self._db.keys())

        return 0

    def commit(self) -> None:
        """
        Commit changes to the database.
        """

        self._db.commit()

    def close(self) -> None:
        """
        Close the database.
        """

        self._db.close()

    def add(self, data: str | bytes) -> int:
        """
        Add a new item to the database.

        :param bytes data: The data to add.
        :return: The ID of the item.
        """

        # PERF: Deduplicate items

        self._db[self.max_index + 1] = {"data": data}

        return 1

    def query(self, item_id: int) -> bytes | str:
        """
        Search the database for an item using its ID.

        :param int id: The ID of the item.
        :return: The contents of the item.
        """

        return self._db[item_id]

    def delete(self, item_id: int) -> None:
        """
        Delete an item from the database.
        :param int id: The ID of the item.
        """

        del self._db[item_id]

    def wipe(self) -> None:
        """
        Wipe the database contents.
        """

        self._db.clear()

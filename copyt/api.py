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

import pathlib

from copyt import _db_manager
from copyt.models.clipboard_record import ClipboardRecord
from copyt.models.global_options import GlobalOptions


class API:
    """
    The API for working with copyt
    """

    def __init__(
        self,
        global_options: GlobalOptions,
    ):
        """
        :param str cache_dir: The directory where the cache is stored.
        """

        self.global_options = global_options
        self.db_manager = _db_manager.DBManager(self.history_file)

    @property
    def history_file(self) -> pathlib.Path:
        """
        The database file for the history.
        """

        return pathlib.Path(self.global_options.cache_dir, "history.db")

    def commit(self) -> None:
        """
        Commit changes to the database.
        """

        self.db_manager.commit()

    def close(self, commit: bool = False) -> None:
        """
        Close the database.
        """

        if commit:
            self.commit()

        self.db_manager.close()

    def store(self, data: str | bytes) -> int:
        """
        Store data to history.

        :param str | bytes data: The data to store.
        :return: The ID of the item.
        """

        if len(data) > self.global_options.max_item_size_in_bytes:
            raise ValueError(
                "The size of the data is larger than the maximum allowed size"
            )

        return self.db_manager.add(data)

    def remove(self, item_id: int) -> None:
        """
        Remove an item from the history.

        :param int item_id: The ID of the item to remove.
        """

        self.db_manager.delete(item_id)

    def remove_last(self) -> None:
        """
        Remove the last item from the history.
        """

        self.db_manager.delete(self.db_manager.max_index)

    def wipe(self) -> None:
        """
        Wipe the history.
        """

        self.db_manager.wipe()

    def get_history_list(self) -> list[tuple[str, ClipboardRecord]]:
        """
        Get a list of all items in the history.
        """

        return self.db_manager.get_all()

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

from copyt.global_options import GlobalOptions


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

    @property
    def history_file(self) -> pathlib.Path:
        """
        The database file for the history.
        """

        return pathlib.Path(self.global_options.cache_dir, "history.db")

    def store(self, data: str | bytes) -> None:
        """
        Store data to history.
        """

        if isinstance(data, str):
            data = data.encode(self.global_options.text_encoding)

        # TODO: This is just a placeholder.
        with open(self.history_file, "wb") as f:
            f.write(data)

    def remove(self):
        pass

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
import sys
from typing import Optional


def get_program_cache_dir(cache_dir: str | pathlib.Path) -> pathlib.Path:
    """
    Make <cache_dir>/<program_cache_dir>

    :param str | pathlib.Path cache_dir: The directory where the cache should be stored.
    :return: The directory where the program cache is stored.
    """

    return pathlib.Path(cache_dir, "copyt")


def get_input_from_arg_or_stdin(arg: Optional[str] = None) -> str | bytes | None:
    """
    Get input from argument or stdin. Argument takes precedence over stdin.

    :param Optional[str] arg: The argument to get the input from.
    """

    if arg is not None:
        return arg

    if not sys.stdin.buffer.isatty():
        stdin_data = sys.stdin.buffer.read()
        if len(stdin_data) > 0:
            return stdin_data

    return None

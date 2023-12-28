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
import sys
from typing import Optional

import typer
from typing_extensions import Annotated

from copyt import api, helpers, info
from copyt.global_options import GlobalOptions

cmd = typer.Typer()
global_options: GlobalOptions = GlobalOptions(
    json=False,
    max_items=750,
    verbose=False,
    cache_dir=helpers.get_program_cache_dir(
        os.getenv("XDG_CACHE_HOME") or pathlib.Path(pathlib.Path.home(), ".cache")
    ),
    text_encoding="utf-8",
)


@cmd.callback()
def main_callback(
    json: bool = global_options.json,
    max_items: int = global_options.max_items,
    verbose: bool = global_options.verbose,
    cache_path: Optional[str] = None,
    text_encoding: str = global_options.text_encoding,
):
    """
    Setup global options
    """

    global_options.json = json
    global_options.max_items = max_items
    global_options.verbose = verbose
    global_options.cache_dir = cache_path or global_options.cache_dir
    global_options.text_encoding = text_encoding


@cmd.command(name="version")
def cmd_version():
    """
    Show the version and exit
    """

    print(f"{info.NAME} v{'.'.join(map(str,info.VERSION))}")
    raise typer.Exit(0)


@cmd.command(name="store")
def cmd_store(data: Annotated[Optional[str], typer.Argument()] = None):
    """
    Store something in the clipboard
    """

    copyt_api = api.API(global_options)
    if data is not None:
        copyt_api.store(data)

    elif not sys.stdin.buffer.isatty():
        copyt_api.store(sys.stdin.buffer.read())

    else:
        typer.echo("Nothing to store", err=True)
        raise typer.Exit(10)


@cmd.command(name="list", help="Get a list of all stored items")
def cmd_list(sep: str = "\t"):
    # TODO
    print("command: list")


@cmd.command(name="decode", help="Get something from the clipboard")
def cmd_decode(something: Annotated[Optional[str], typer.Argument()] = None):
    # TODO
    print(f"command: decode `{something}` from clipboard")


@cmd.command(name="delete", help="Delete something from the clipboard")
def cmd_delete(something: Annotated[Optional[str], typer.Argument()] = None):
    # TODO
    print(f"command: delete `{something}` from clipboard")


@cmd.command(name="wipe", help="Wipe the clipboard history")
def cmd_wipe():
    # TODO
    print("command: wipe")

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
import pathlib
import sys
from typing import Optional

import magic
import typer
from typing_extensions import Annotated

from copyt import api, helpers, info
from copyt.models.global_options import GlobalOptions

cmd = typer.Typer()
global_options: GlobalOptions = GlobalOptions(
    json=False,
    max_items=750,
    max_item_size_in_bytes=1024 * 1024 * 5,  # 5MB
    verbose=False,
    cache_dir=helpers.get_program_cache_dir(
        os.getenv("XDG_CACHE_HOME") or pathlib.Path(pathlib.Path.home(), ".cache")
    ),
    text_encoding="utf-8",
)


@cmd.callback()
def main_callback(  # pylint: disable=R0913
    json_output: Annotated[bool, typer.Option("--json", "-j")] = global_options.json,
    max_items: Annotated[
        int, typer.Option("--max-items", "-m")
    ] = global_options.max_items,
    max_item_size: Annotated[
        int, typer.Option("--max-item-size", "-s")
    ] = global_options.max_item_size_in_bytes,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = global_options.verbose,
    cache_dir: Annotated[Optional[str], typer.Option("--cache-dir", "-c")] = None,
    text_encoding: Annotated[
        str, typer.Option("--encoding", "-e")
    ] = global_options.text_encoding,
):
    """
    Setup global options
    """

    global_options.json = json_output
    global_options.max_items = max_items
    global_options.max_item_size_in_bytes = max_item_size
    global_options.verbose = verbose
    global_options.cache_dir = cache_dir or global_options.cache_dir
    global_options.text_encoding = text_encoding


@cmd.command(name="version")
def cmd_version():
    """
    Show the version and exit
    """

    print(
        json.dumps({"name": info.NAME, "version": info.VERSION})
        if global_options.json
        else f"{info.NAME} v{'.'.join(map(str,info.VERSION))}"
    )

    raise typer.Exit(0)


@cmd.command(name="store")
def cmd_store(data: Annotated[Optional[str], typer.Argument()] = None):
    """
    Store something in the clipboard
    """

    copyt_api = api.API(global_options)

    # data from argument
    if data is not None:
        copyt_api.store(data)
        copyt_api.close(commit=True)
        raise typer.Exit(0)

    # data from stdin
    if not sys.stdin.buffer.isatty():
        stdin_data = sys.stdin.buffer.read()
        if len(stdin_data) > 0:
            copyt_api.store(stdin_data)
            copyt_api.close(commit=True)
            raise typer.Exit(0)

    typer.echo("Nothing to store", err=True)
    raise typer.Exit(10)


@cmd.command(name="list")
def cmd_list(
    output_format: Annotated[
        str,
        typer.Option(help="Set a custom format of the output."),
    ] = "[{id}]\t{content}"
):
    """
    Get a list of all stored items
    """

    copyt_api = api.API(global_options)
    hist_list = copyt_api.get_history_list()
    for item_id, data in hist_list:
        print(
            # DOCS: document the behavior of this
            output_format.format(
                id=item_id,
                kind=magic.from_buffer(data.content, mime=True),
                content=magic.from_buffer(data.content)
                if isinstance(data.content, bytes)
                else data.content,
                size=len(data.content),
                timestamp=data.timestamp.timestamp,
            )
        )

    copyt_api.close()

    raise typer.Exit(0)


@cmd.command(name="decode", help="Get something from the clipboard")
def cmd_decode(something: Annotated[Optional[str], typer.Argument()] = None):
    # TODO
    print(f"command: decode `{something}` from clipboard")


@cmd.command(name="delete", help="Delete something from the clipboard")
def cmd_delete(something: Annotated[Optional[str], typer.Argument()] = None):
    # TODO
    print(f"command: delete `{something}` from clipboard")


@cmd.command(name="wipe")
def cmd_wipe():
    """
    Wipe the clipboard history
    """

    copyt_api = api.API(global_options)
    copyt_api.wipe()
    copyt_api.close(commit=True)
    typer.echo("Wiped the clipboard history.")
    raise typer.Exit(0)

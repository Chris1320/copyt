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


from typing import Optional

import typer
from typing_extensions import Annotated

from copyt import info

cmd = typer.Typer()
global_options = {}


@cmd.callback()
def main_callback(
    json: bool = False,
    max_items: int = 750,
    verbose: bool = False,
):
    """
    Setup global options
    """

    global_options["json"] = json
    global_options["max_items"] = max_items
    global_options["verbose"] = verbose


@cmd.command(name="version")
def cmd_version():
    """
    Show the version and exit
    """

    print(f"{info.NAME} v{'.'.join(map(str,info.VERSION))}")
    raise typer.Exit()


@cmd.command(name="store", help="Store something in the clipboard")
def cmd_store(something: Annotated[Optional[str], typer.Argument()] = None):
    # TODO
    print(f"command: store `{something}` to clipboard")


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

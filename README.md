# copyt

_Copy It!_ — Another clipboard manager for Wayland

> **NOTE**: This project is currently under development.

## Usage

Usage: `copyt [OPTIONS] COMMAND [ARGS]...`

### Options

| Long Form              | Short Form | Description                                                                                      |
| ---------------------- | ---------- | ------------------------------------------------------------------------------------------------ |
| `--help`               |            | Show this message and exit.                                                                      |
|                        |            |                                                                                                  |
| `--max-items=<n>`      | `-m <n>`   | The amount of clipboard records to store in history. (default: `750`)                            |
| `--max-item-size=<n>`  | `-s <n>`   | The maximum size (in bytes) of data to be allowed in the clipboard history. (default: `5242880`) |
|                        |            |                                                                                                  |
| `--json`               | `-j`       | Show output in JSON.                                                                             |
| `--verbose`            | `-v`       | Enable verbose mode.                                                                             |
| `--encoding=<s>`       | `-e <s>`   | The text encoding to use. (default: `utf-8`)                                                     |
| `--cache-dir=<dir>`    | `-c <dir>` | Set a custom location for the history file. (default: `~/.cache/copyt`)                          |
|                        |            |                                                                                                  |
| `--install-completion` |            | Install completion for the current shell.                                                        |
| `--show-completion`    |            | Show completion for the current shell, to copy it or customize the installation.                 |

### Commands

| Command   | Description                         |
| --------- | ----------------------------------- |
| `store`   | Store something in the clipboard    |
| `list`    | Get a list of all stored items      |
| `get`     | Get something from the clipboard    |
| `delete`  | Delete something from the clipboard |
| `wipe`    | Wipe the clipboard history          |
|           |                                     |
| `version` | Show the version and exit           |

**Example Usage**:

```bash
copyt store "foo"                        # [1] add `foo` to the history.
printf "bar" | copyt store               # [2] you can also pipe data to copyt
cat ./image.png | copyt store            # [3] pipe binary data to copyt
printf '{"spam": "eggs"}' | copyt store

copyt list  # list all stored data
# sample output:
#
# 1       foo
# 2       bar
# 3       PNG image data, 1719 x 1920, 8-bit/color RGBA, non-interlaced
# 4       {"foo": "bar"}

copyt get 2  # output: bar
copyt get 3 > image-from-copyt.png  # output the stored image to file
copyt --json get 1 | jq -r ".timestamp"  # set output to JSON and get the
                                         # timestamp of the specified item

copyt delete 3  # delete item 3 from the history.
copyt wipe  # delete all items in the history.

# set copyt as your clipboard manager
wl-paste --type text --watch copyt store
wl-paste --type image --watch copyt store
```

---

_copyt is heavily inspired by [cliphist](https://github.com/sentriz/cliphist)_.

# e7impress utils

This is a parser for e7impress files.
The song lyrics can be output as json or plain text.

## setup

You need to install the following dependencies package from your favorite
python package manager.

- click
- pydantic

## command line utilities

The is a command-line program `e7` can be used to create scripts.

Example (in your shell):

```shell
$ ./e7 parse path/to/file.7is
$ ./e7 parse -f txt path/to/file.7is
$ ./e7 parse -o output.json path/to/file.7is
```

The resulting json files can be loaded and printed as txt:

```shell
$ ./e7 load output.json
```

### full command line syntax

```shell
$ ./e7 --help
Usage: e7 [OPTIONS] COMMAND [ARGS]...

  Initialize the cli context.

Options:
  --debug / --no-debug
  --help                Show this message and exit.

Commands:
  load   Load a `Song` file.
  parse  Parse an e7impress file.

$ ./e7 load --help
Usage: e7 load [OPTIONS] FILENAME

  Load a `Song` file.

Options:
  -f, --format [txt|json]  The output format
  --help                   Show this message and exit.

$ ./e7 parse --help
Usage: e7 parse [OPTIONS] FILENAME

  Parse an e7impress file.

Options:
  -f, --format [txt|json]  The output format.
  -o, --output TEXT        The output file. If no filename is given, the
                           result iswritten to stdout.

  --help                   Show this message and exit.
```

## e7parser

You can load and parse a file like this:

```python
from e7parser import E7File

e7file = E7File('path/to/file.7is')
song = e7file.get_song()
```

The `Song` class contains all relevant info.
This is the schema:

```python
class Verse:
    name: str
    text: str

class Song:
    order: List[str]  # List of verse names in order
    verses: List[Verse]  # All verses in the song
    title: str
```

A `Song` object can be written into a file, like this:

```python
song.save('filename.json')
```

The file can also be loaded:

```python
song = Song.load('filename.json')
```

A `Song` object returns the whole Song, in order, with the following command:

```python
song.txt()
```

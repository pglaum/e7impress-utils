# e7impress utils

This is a parser for e7impress files.
The song can be written into a json file, for easy usage with further content.

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

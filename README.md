# e7impress parser

This is a parser for e7impress files.
The song can be written into a json file, for easy usage with further content.

## Setup

You need to install the `pydantic` package from your favorite python package
manager.

## Usage

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

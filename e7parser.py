from pydantic import BaseModel
from typing import Any, Dict, List
import json
import os


class Verse(BaseModel):

    name: str
    text: str

    def __repr__(self) -> str:

        return f'<Verse: {self.name}>'


class Song(BaseModel):

    # List of verses in order. Must use the `name` field of the verses.
    order: List[str]

    verses: List[Verse]  # All distinct verses in the song
    title: str

    def save(self, filename: str) -> bool:
        """Save the Song object into a json file.
        """

        try:
            with open(filename, 'w') as f:
                f.write(self.json())

            return True

        except Exception as e:
            print(f'error: could not save song ({e})')

        return False

    @staticmethod
    def load(filename: str) -> Any:
        """Load a Song object from a json file.
        """

        if not os.path.isfile(filename):
            print('error could not load song (file does not exist)')

        try:
            with open(filename, 'r') as f:
                content = f.read()

            data = json.loads(content)
            song = Song(**data)
            return song

        except Exception as e:
            print(f'error: could not load song ({e})')

        return None

    def txt(self) -> str:
        """Get a formatted string text of the whole song.
        """

        res = ''

        for item in self.order:

            found = False
            for verse in self.verses:
                if verse.name == item:
                    res += f'{verse.name}:\r\n'
                    res += verse.text
                    if not res.endswith('\r\n'):
                        res += '\r\n'
                    res += '\r\n'

                    found = True
                    break

            if not found:
                res += f'{item}:\r\n'
                res += 'Error: not found!\r\n\r\n'

        while res.endswith('\r\n'):
            res = res[:-2]

        return res

    def __repr__(self) -> str:

        return f'<Song: {self.title}>'


class E7File:

    def __init__(self, filename: str) -> None:
        """Initialize an E7File object.
        """

        self.__filename = filename
        self.__content = ''
        self.__fields: Dict[str, str] = {}

        self.__load()

    def __load(self) -> None:
        """Load and sanitize the file contents.
        """

        if not self.__content:
            try:
                with open(self.__filename, 'rb') as f:
                    bytes_content = f.read()

                self.__content = bytes_content.decode('iso_8859_1')

                # sanitize this one field, somehow it doesnt work otherwise...
                self.__content = self.__content.replace(
                    'type:e7impress.song5Dcontent',
                    'type:e7impress.song5  Dcontent')

            except Exception as e:
                print(f'error: could not load file ({e})')

    def __check(self, include_fields: bool = False) -> bool:
        """Check if the object is correctly setup and all necessary fields are
        available.
        """

        if not os.path.isfile(self.__filename):
            print(f'error: file does not exist ({self.__filename})')
            return False

        if not self.__content:
            self.__load()

            if not self.__content:
                print('error: could not load file')
                return False

        if 'type:e7impress.song' not in self.__content:
            print(f'error: invalid file contents ({self.__filename})')
            return False

        if include_fields and (not self.__fields or len(self.__fields) < 1):
            self.__parse()
            if not self.__fields:
                print('error: could not load fields')

        return True

    def __cut_out(self, start: int, length: int) -> str:

        # Somehow the starting position is at -1, usually.
        # Because we add 2 spaces in the `__load` position, we have to add +2
        start = start + 1

        return self.__content[start:start+length]

    def __make_fields(self, text: str) -> Dict[str, str]:
        """Load a key/value dict from plain texts.
        """

        res = {}

        items = text.split('  ')
        items = [item.strip() for item in items if item]

        length = len(items)
        for i in range(length - 1):

            if i > (length - 2):
                break

            cur_item = items[i]
            next_item = items[i+1]

            if len(next_item) == 20 and next_item.isdigit():

                start = int(next_item[:10])
                slen = int(next_item[10:])
                content = self.__cut_out(start, slen)

                # NOTE: fields with identical keys _will_ be overwritten
                res[cur_item] = content

                i = i + 1

        return res

    def __parse(self) -> None:
        """Load the main fields of the file.
        """

        if not self.__check():
            return

        # the first line contains the interesting fields
        first_line = self.__content.splitlines()[0]

        self.__fields = self.__make_fields(first_line)

    def get_content(self) -> str:
        """Get loaded file contents.
        """

        return self.__content

    def get_fields(self) -> Dict[str, str]:
        """Get the main fields.
        """

        return self.__fields

    def get_order(self) -> List[str]:
        """Get the order of verses.
        """

        if not self.__check(True):
            return []

        text = self.__fields['Fablauf']
        items = [i.strip() for i in text.split('\x01') if i]

        return items

    def get_namespaces(self) -> Dict[str, str]:
        """Get the namespaces.

        Namespaces are the reference for the names of the verses.
        """

        if not self.__check(True):
            return {}

        text = self.__fields['Dnamespace']
        fields = self.__make_fields(text)

        return fields

    def get_verses(self) -> List[Verse]:
        """Get the verses in the song.
        """

        if not self.__check(True):
            return []

        text = self.__fields['Dcontent']
        fields = self.__make_fields(text)
        for k, v in fields.items():
            fields[k] = v.strip()

        verses = []
        namespaces = self.get_namespaces()

        for k, v in namespaces.items():
            try:
                verses.append(Verse(name=v, text=fields[k]))
            except Exception:
                print(f'error: verse not found ({k}: {v})')

        return verses

    def get_song(self) -> Song:
        """Get the song object for the file.
        """

        verses = self.get_verses()
        order = self.get_order()

        title = self.__filename
        title = os.path.basename(title)
        title = os.path.splitext(title)[0]

        song = Song(title=title, order=order, verses=verses)

        return song

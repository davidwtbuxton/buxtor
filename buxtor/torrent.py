import collections
import os
from datetime import datetime, timezone

from . import bencode
from . import utils


UTF8 = 'UTF-8'
_File = collections.namedtuple('File', ['length', 'path'])


class File(_File):
    @classmethod
    def from_torrent_files(cls, name, data):
        length = data[b'length']
        name = name.decode(UTF8)
        path = os.path.join(name, *(part.decode(UTF8) for part in data[b'path']))

        return cls(length=length, path=path)

    @classmethod
    def from_torrent_info(cls, data):
        """Returns a list of File objects.

        `data` is the torrent's 'info' dict.
        """
        name = data[b'name']

        if b'length' in data:
            name = name.decode(UTF8)
            files = [cls(length=data[b'length'], path=name)]
        else:
            files = [cls.from_torrent_files(name, data[b'files'])]

        return files


class Torrent(object):
    def __init__(self, announce_list, creation_date, comment, files,
            piece_length, pieces):
        self.announce_list = announce_list or [] # 'announce', a string or a list of strings.
        self.comment = comment
        self.created_by = '' # 'created by'
        self.creation_date = creation_date # Converted from a unix timestamp.
        self.encoding = '' # Text encoding.
        self.files = files # ''
        self.piece_length = piece_length
        self.pieces = pieces


def from_string(value):
    data = bencode.decode(value)

    if b'announce-list' in data:
        # Multi-tracker extension http://bittorrent.org/beps/bep_0012.html
        announce_list = data[b'announce-list']
    else:
        announce_list = [data[b'announce']]

    if b'creation date' in data:
        creation_date = data[b'creation date']
        creation_date = datetime.fromtimestamp(creation_date, timezone.utc)
    else:
        creation_date = None

    comment = data[b'comment']

    # A single file has a 'length' key, multiple files have 'files'.
    info = data[b'info']
    files = File.from_torrent_info(info)
    piece_length = info[b'piece length']
    pieces = info[b'pieces']

    hashes = list(utils.grouper(pieces, 20))

    return Torrent(announce_list=announce_list, creation_date=creation_date,
        comment=comment, files=files, piece_length=piece_length, pieces=pieces)


def from_directory(path):
    """Returns a new Torrent instance for the files in a directory."""
    for filename in utils.walk_dir(path):
        pass

    return Torrent()


def from_file(path):
    """Returns a new Torrent instance for one file."""

    return Torrent()


if __name__ == '__main__':
    import pprint
    import sys

    with open(sys.argv[1], 'rb') as fh:
        value = fh.read()
        torrent = from_string(value)

        pprint.pprint(torrent)

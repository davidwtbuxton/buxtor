import hashlib
import unittest
from datetime import datetime, timezone

from buxtor import bencode, torrent


one_megabyte = 2 ** 20

torrent_data = {
    'announce': 'http://example.com/',
    'comment': 'Example comment',
    'creation date': int(datetime(1999, 12, 31, tzinfo=timezone.utc).timestamp()),
    'info': {
        'name': 'Example name',
        'length': one_megabyte,
        'piece length': one_megabyte,
        'pieces': hashlib.sha1(b'example').digest(),
    },
}


class FromStringTestCase(unittest.TestCase):
    def test_from_string(self):
        value = bencode.encode(torrent_data)
        result = torrent.from_string(value)

        self.assertIsInstance(result, torrent.Torrent)
        self.assertEqual(
            result.__dict__,
            {
                'announce_list': [b'http://example.com/'],
                'comment': b'Example comment',
                'created_by': '',
                'creation_date': datetime(1999, 12, 31, 0, 0, tzinfo=timezone.utc),
                'encoding': '',
                'files': [torrent.File(length=1048576, path='Example name')],
                'piece_length': 1048576,
                'pieces': b"\xc3I\x9c')s\n\x7f\x80~\xfb\x86v\xa9-\xcbo\x8a?\x8f",
            },
        )

Buxtor
======

Read / write [bencode data in BitTorrent files][bep3]. Works with Python 3.4 or later.

This library handles nested data structures and unicode strings. It _should_ be 100% compliant with the specification. If it isn't, please file a bug.

The [source code and issue tracker][home] are on GitHub.


Usage
-----

    >>> import buxtor.bencode

Encode basic Python data types with `buxtor.bencode.encode`:

    >>> buxtor.bencode.encode({'spam': ['a', 'b']})
    b'd4:spaml1:a1:bee'

Decode a bencoded byte string with `buxtor.bencode.decode`:

    >>> buxtor.bencode.decode(b'd4:spaml1:a1:bee')
    {'spam': ['a', 'b']}

Encoding types other than `str`, `list`, `tuple`, `dict`, `int`, and `bool` will raise a TypeError exception:

    >>> buxtor.bencode.encode({1, 2, 3})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/jimmy/buxtor/bencode.py", line 92, in encode
        raise TypeError('Cannot encode type %s' % type(obj))
    TypeError: Cannot encode type <class 'set'>


[bep3]: http://www.bittorrent.org/beps/bep_0003.html
[home]: https://github.com/davidwtbuxton/buxtor

import itertools


def decode(value):
    """Decodes a torrent and returns a Python object."""
    assert isinstance(value, bytes), 'Argument must be of type %r' % bytes

    iter_val = iter(value)

    return _decode(iter_val)


def _decode(iter_val):
    c = next(iter_val)

    if c == ord('e'):
        # This was a dict or list and there are no more items.
        return None

    elif c == ord('i'):
        # Integer.
        chars = itertools.takewhile(lambda c: c != ord('e'), iter_val)
        value = bytes(chars).decode('ascii')

        return int(value)

    elif c == ord('d'):
        # Dictionary, possibly empty.
        value = {}

        while True:
            k = _decode(iter_val)

            if k is None:
                return value

            value[k] = _decode(iter_val)

    elif c == ord('l'):
        # List, possibly empty.
        value = []

        while True:
            v = _decode(iter_val)

            if v is None:
                return value

            value.append(v)

    else:
        # Only other type is a string.
        chars = itertools.takewhile(lambda c: c != ord(':'), iter_val)
        length = (bytes([c]) + bytes(chars)).decode('ascii')
        length = int(length)

        value = itertools.islice(iter_val, 0, length)
        value = bytes(value).decode('utf-8')

        return value


def encode(obj):
    """Encodes a Python object and returns a byte string."""
    if isinstance(obj, str):
        str_value = obj.encode('utf-8')
        str_length = len(str_value)

        return str(str_length).encode('utf-8') + b':' + str_value

    elif isinstance(obj, int):
        # Also handles True and False.
        obj = int(obj)

        return b'i' + str(obj).encode('utf-8') + b'e'

    elif isinstance(obj, (list, tuple)):
        contents = (encode(o) for o in obj)

        return b'l' + b''.join(contents) + b'e'

    elif isinstance(obj, dict):
        contents = []

        for k in sorted(obj):
            contents.append(encode(k))
            contents.append(encode(obj[k]))

        return b'd' + b''.join(contents) + b'e'

    else:
        raise TypeError('Cannot encode type %s' % type(obj))

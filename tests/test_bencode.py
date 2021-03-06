import unittest

from buxtor import bencode


class DecoderTestCase(unittest.TestCase):
    def test_decodes_string(self):
        result = bencode.decode(b'3:foo')

        self.assertEqual(result, b'foo')

    def test_decodes_integer(self):
        result = bencode.decode(b'i999e')

        self.assertEqual(result, 999)

    def test_decodes_negative_integer(self):
        result = bencode.decode(b'i-999e')

        self.assertEqual(result, -999)

    def test_decodes_list(self):
        result = bencode.decode(b'l3:foo3:bare')

        self.assertEqual(result, [b'foo', b'bar'])

    def test_decodes_dict(self):
        result = bencode.decode(b'd4:spaml1:a1:bee')

        self.assertEqual(result, {b'spam': [b'a', b'b']})

    def test_decodes_dict_with_long_keys(self):
        result = bencode.decode(b'd19:the quick brown foxi1ee')

        self.assertEqual(result, {b'the quick brown fox': 1})

    def test_errors_for_str_input(self):
        with self.assertRaisesRegex(AssertionError, 'Argument must be of type'):
            bencode.decode('3:foo')


class EncodeTestCase(unittest.TestCase):
    def test_encodes_string(self):
        result = bencode.encode(u'foo')

        self.assertEqual(result, b'3:foo')

    def test_encodes_positive_integer(self):
        result = bencode.encode(999)

        self.assertEqual(result, b'i999e')

    def test_encodes_negative_integer(self):
        result = bencode.encode(-999)

        self.assertEqual(result, b'i-999e')

    def test_encodes_list(self):
        result = bencode.encode([u'foo', u'bar'])

        self.assertEqual(result, b'l3:foo3:bare')

    def test_encodes_dict(self):
        result = bencode.encode({u'spam': [u'a', u'b']})

        self.assertEqual(result, b'd4:spaml1:a1:bee')

    def test_encodes_dict_with_long_keys(self):
        result = bencode.encode({u'the quick brown fox': True})

        self.assertEqual(result, b'd19:the quick brown foxi1ee')

    def test_errors_for_incompatible_types(self):
        with self.assertRaisesRegex(TypeError, 'Cannot encode type'):
            bencode.encode(1.0)


if __name__ == '__main__':
    unittest.main()

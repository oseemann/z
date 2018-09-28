import unittest


def find_shorttest_distance(doc, a, b):
    # Keep only alphanumeric and whitespace characters, removes punctuation
    doc_alnum = ''.join(c for c in doc if c.isalnum() or c.isspace())

    # Split doc into list of words
    words = doc_alnum.split()

    # Lists to store positions of search arguments a and b
    pos_a = []
    pos_b = []

    # Find where both words appear in the doc
    for i in range(len(words)):
        if words[i] == a:
            pos_a.append(i)
        elif words[i] == b:
            pos_b.append(i)

    # Find shortest distance of word positions
    distances = [abs(pb - pa) - 1 for pa in pos_a for pb in pos_b]

    return min(distances) if distances else None


class Test(unittest.TestCase):

    def t(self, doc, a, b, dist):
        self.assertEqual(find_shorttest_distance(doc, a, b), dist)

    def test_simple(self):
        self.t('a', 'a', 'a', None)
        self.t('a', 'a', 'b', None)
        self.t('a b', 'a', 'b', 0)
        self.t('a b c', 'a', 'b', 0)
        self.t('a b c', 'a', 'c', 1)
        self.t('a b c d', 'a', 'b', 0)
        self.t('a b c d', 'a', 'c', 1)
        self.t('a b c d', 'a', 'd', 2)
        self.t('a b c d', 'b', 'b', None)

    def test_reverse(self):
        self.t('a b c d', 'd', 'a', 2)
        self.t('a b c d', 'c', 'a', 1)
        self.t('a b c d', 'b', 'a', 0)
        self.t('a b c d', 'c', 'b', 0)


if __name__ == '__main__':
    unittest.main()

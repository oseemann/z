import sys
import unittest


def find_shorttest_distance(doc: str, a: str, b: str) -> int:
    """
    Return number of words in the document `doc` that occur between the words
    `a` and `b`.

    All punctionation is ignored and case is insensitive.
    Order of occurences does not matter. I.e. a word2 occuring before word1
    will also result in a positive distance and not a negative one.

    @param doc: A document to search in
    @param a: First keyword
    @param b: Second keyword

    @return Number of words or None if no match is found or a and b are equal
    """
    # Keep only alphanumeric and whitespace characters, removes punctuation
    doc_alnum = ''.join(c.lower() for c in doc if c.isalnum() or c.isspace())

    # Split doc into list of words
    words = doc_alnum.split()

    # Lists to store positions of search arguments a and b
    pos_a = []
    pos_b = []
    low_a = a.lower()
    low_b = b.lower()

    # Find where both words appear in the doc
    for i in range(len(words)):
        if words[i] == low_a:
            pos_a.append(i)
        elif words[i] == low_b:
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

    def test_case(self):
        self.t('A B c D', 'a', 'd', 2)
        self.t('A B c D', 'C', 'a', 1)

    def test_zageno_example(self):
        d = 'We do value and reward motivation in our development team. '\
            'Development is a key skill for a DevOp.'
        self.t(d, 'motivation', 'development', 2)
        self.t(d, 'We', 'do', 0)
        self.t(d, 'we', 'DO', 0)
        self.t(d, 'DevOp', 'we', 16)
        self.t(d, 'value', 'skill', 11)
        self.t(d, 'team', 'DEVELOPMENT', 0)

    def test_many_duplicate_words(self):
        d = 'A B G A A B G F B B E G A C C F B G D F B'
        self.t(d, 'A', 'B', 0)
        self.t(d, 'A', 'C', 0)
        self.t(d, 'A', 'D', 5)
        self.t(d, 'A', 'E', 1)
        self.t(d, 'A', 'F', 2)
        self.t(d, 'A', 'G', 0)

        d = 'D J J F P H D B D Q R M Q M O N O J O K P L K D L Q E Q C S'
        self.t(d, 'D', 'O', 4)
        self.t(d, 'K', 'Q', 2)
        self.t(d, 'S', 'F', 25)


def run(args):
    try:
        doc = open(args[1]).read()
        a = args[2]
        b = args[3]
    except IndexError as e:
        print("Usage: distance.py file word1 word2")
        print("Example: distance.py test.txt Roads I")
        return
    except IOError as e:
        print('File `{}` cannot be opened'.format(args[1]))
        return

    dist = find_shorttest_distance(doc, a, b)
    if dist is None:
        msg = 'Not found. Either `{a}` or `{b}` have not been found in the doc'
    else:
        msg = 'Distance between `{a}` and `{b}` is {dist} words'
    print(msg.format(**locals()))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(sys.argv)
    else:
        unittest.main(verbosity=2)

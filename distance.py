import sys
import unittest


def find_shorttest_distance(doc: str, a: str, b: str, slow: bool = False) -> int:
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

    if slow:
        return find_quadratic(words, a.lower(), b.lower())
    else:
        return find_linear(words, a.lower(), b.lower())


def find_quadratic(words: str, w1: str, w2: str):
    """
    Sub-optimal implementation of the distance search.

    It generates a list of all search word positions and then finds the
    shortest difference of all position combinations.

    For search words that appear only infrequently in the document this is not
    a problem: the position lists will be short.
    However when both search words appear very frequently, the complexity of
    this function becomes quadratic (of the search word frequency, not the
    number of total words).
    """
    # Lists to store positions of search words a and b
    pos_w1 = []
    pos_w2 = []

    # Find where both words appear in the doc
    for i in range(len(words)):
        if words[i] == w1:
            pos_w1.append(i)
        elif words[i] == w2:
            pos_w2.append(i)

    # Calculate distances for all found combinations of positions
    # For search words with very high frequency in the document this will be
    # slow, as the product of all position pairs is generated.
    distances = [abs(pos1 - pos2) - 1 for pos1 in pos_w1 for pos2 in pos_w2]

    # Return minimum distance
    return min(distances) if distances else None


def find_linear(words: str, w1: str, w2: str):
    """
    An implementation with linear complexity that iterates over all words only
    once.
    """
    mindist = None
    pos_w1 = None
    pos_w2 = None
    for i in range(len(words)):
        w = words[i]

        # Update last known positions of the search words
        if w == w1:
            pos_w1 = i
        elif w == w2:
            pos_w2 = i
        else:
            # Not a search word, skip
            continue

        if pos_w1 is None or pos_w2 is None:
            # Have not yet found both words
            continue

        # When this is reached, a new occurence of a search word has been
        # found. Let's calculate the distance.
        dist = abs(pos_w1 - pos_w2) - 1

        # Is this distance shorter than the one we have found so far?
        if mindist is None or dist < mindist:
            # Yes, remember this one
            mindist = dist

    return mindist


class Test(unittest.TestCase):

    def t(self, doc, a, b, dist):
        self.assertEqual(find_shorttest_distance(doc, a, b), dist)
        self.assertEqual(find_shorttest_distance(doc, a, b, slow=True), dist)

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
        w1 = args[2]
        w2 = args[3]
    except IndexError as e:
        print("Usage: distance.py file word1 word2")
        print("Example: distance.py test.txt Roads I")
        return
    except IOError as e:
        print('File `{}` cannot be opened'.format(args[1]))
        return

    dist = find_shorttest_distance(doc, w1, w2)
    if dist is None:
        msg = '404: Either `{w1}` or `{w2}` have not been found in the doc'
    else:
        msg = 'Distance between `{w1}` and `{w2}` is {dist} words'
    print(msg.format(**locals()))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(sys.argv)
    else:
        unittest.main(verbosity=2)

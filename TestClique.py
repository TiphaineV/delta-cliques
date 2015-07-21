import unittest
from CliqueMaster import CliqueMaster
from Clique import Clique
from collections import deque
import sys
import os


class TestClique(unittest.TestCase):

    def setUp(self):
        self.Cm = CliqueMaster()
        self.seq = range(10)
        sys.stderr = open(os.devnull, 'w')

    def test_delta_is_0(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1)))
        ])
        self.Cm._times = {frozenset([1, 2]): [1]}
        self.Cm._nodes = {1: set([2]), 2: set([1])}
        R = self.Cm.getDeltaCliques(0)
        self.assertEqual(R, set([Clique((frozenset([1, 2]), (1, 1)))]))

    def test_negative_delta(self):
        pass

    def test_big_delta(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1)))
        ])
        self.Cm._times = {frozenset([1, 2]): [1]}
        self.Cm._nodes = {1: set([2]), 2: set([1])}
        R = self.Cm.getDeltaCliques(100)
        self.assertEqual(R, set([Clique((frozenset([1, 2]), (-99, 101)))]))

    def test_simple_triangle_when_delta_is_5(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1))),
            Clique((frozenset([1, 3]), (2, 2))),
            Clique((frozenset([2, 3]), (3, 3)))
        ])
        self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
        self.Cm._times = {
            frozenset([1, 3]): [2], frozenset([1, 2]): [1], frozenset([2, 3]): [3]}

        R = self.Cm.getDeltaCliques(5)
        R_expected = set([
            Clique((frozenset([1, 2, 3]), (-2, 6))),
            Clique((frozenset([1, 2]), (-4, 6))),
            Clique((frozenset([2, 3]), (-2, 8))),
            Clique((frozenset([1, 3]), (-3, 7)))
        ])

        debug_msg = "\nGot :\n" + str(self.Cm)
        debug_msg += "\nExpected :\n"
        for c in R_expected:
            debug_msg += str(c) + "\n"
        self.assertEqual(R, R_expected, debug_msg)

    def test_two_links_alterning(self):
        pass

    def test_single_link_occurring_every_delta(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1))),
            Clique((frozenset([1, 2]), (3, 3))),
        ])
        self.Cm._nodes = {1: set([2]), 2: set([1])}
        self.Cm._times = {frozenset([1, 2]): [1, 3]}

        R = self.Cm.getDeltaCliques(3)
        R_expected = set([
            Clique((frozenset([1, 2]), (-2, 6)))
        ])
        self.assertEqual(R, R_expected)

    def test_single_link_not_occurring_every_delta(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1))),
            Clique((frozenset([1, 2]), (3, 3))),
        ])
        self.Cm._nodes = {1: set([2]), 2: set([1])}
        self.Cm._times = {frozenset([1, 2]): [1, 3]}

        R = self.Cm.getDeltaCliques(1)
        R_expected = set([
            Clique((frozenset([1, 2]), (0, 2))),
            Clique((frozenset([1, 2]), (2, 4)))
        ])
        self.assertEqual(R, R_expected)

    def test_triangle_and_many_occurrences_with_delta_too_small(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1))),
            Clique((frozenset([2, 3]), (2, 2))),
            Clique((frozenset([1, 3]), (3, 3))),
            Clique((frozenset([1, 2]), (4, 4))),
        ])
        self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
        self.Cm._times = {
            frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4],
            frozenset([2, 3]): [2]}

        R = self.Cm.getDeltaCliques(2)
        R_expected = set([
            Clique((frozenset([1, 2, 3]), (2, 4))),
            Clique((frozenset([1, 2]), (-1, 3))),
            Clique((frozenset([1, 3]), (1, 5))),
            Clique((frozenset([1, 2, 3]), (1, 3))),
            Clique((frozenset([1, 2]), (2, 6))),
            Clique((frozenset([2, 3]), (0, 4)))
        ])
        debug_msg = "\nGot :\n" + str(self.Cm)
        debug_msg += "\nExpected :\n"
        for c in R_expected:
            debug_msg += str(c) + "\n"

        self.assertEqual(R, R_expected, debug_msg)

    def test_triangle_and_many_occurrences_with_delta_big(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1))),
            Clique((frozenset([2, 3]), (2, 2))),
            Clique((frozenset([1, 3]), (3, 3))),
            Clique((frozenset([1, 2]), (4, 4))),
        ])
        self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
        self.Cm._times = {
            frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4],
            frozenset([2, 3]): [2]}

        R = self.Cm.getDeltaCliques(5)
        R_expected = set([
            Clique((frozenset([1, 2]), (-4, 9))),
            Clique((frozenset([1, 2, 3]), (-2, 7))),
            Clique((frozenset([1, 3]), (-2, 8))),
            Clique((frozenset([2, 3]), (-3, 7)))
        ])
        self.assertEqual(R, R_expected)

    def test_triangle_and_many_occurrences_with_delta_huge(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1))),
            Clique((frozenset([2, 3]), (2, 2))),
            Clique((frozenset([1, 3]), (3, 3))),
            Clique((frozenset([1, 2]), (4, 4)))
        ])
        self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
        self.Cm._times = {
            frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4],
            frozenset([2, 3]): [2]}

        R = self.Cm.getDeltaCliques(100)
        R_expected = set([
            Clique((frozenset([1, 2]), (-99, 104))),
            Clique((frozenset([1, 2, 3]), (-97, 102))),
            Clique((frozenset([1, 3]), (-97, 103))),
            Clique((frozenset([2, 3]), (-98, 102)))
        ])
        debug_msg = "\nGot :\n" + str(self.Cm)
        debug_msg += "\nExpected :\n"
        for c in R_expected:
            debug_msg += str(c) + "\n"
        self.assertEqual(R, R_expected, debug_msg)

    def test_simultaneous_links(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1))),
            Clique((frozenset([2, 3]), (1, 1))),
            Clique((frozenset([1, 3]), (1, 1)))
        ])

        self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
        self.Cm._times = {
            frozenset([1, 2]): [1], frozenset([2, 3]): [1], frozenset([1, 3]): [1]}

        R = self.Cm.getDeltaCliques(5)
        R_expected = set([Clique((frozenset([1, 2, 3]), (-4, 6)))])
        self.assertEqual(R, R_expected)

    def test_simultaneous_links_with_repeat(self):
        self.Cm._S = deque([
            Clique((frozenset([1, 2]), (1, 1))),
            Clique((frozenset([2, 3]), (1, 1))),
            Clique((frozenset([1, 3]), (1, 1))),
            Clique((frozenset([2, 3]), (3, 3)))
        ])

        self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
        self.Cm._times = {
            frozenset([1, 2]): [1], frozenset([2, 3]): [1, 3],
            frozenset([1, 3]): [1]}

        R = self.Cm.getDeltaCliques(5)
        R_expected = set([
            Clique((frozenset([1, 2, 3]), (-4, 6))),
            Clique((frozenset([2, 3]), (-4, 8)))
        ])
        self.assertEqual(R, R_expected)
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClique)
    unittest.TextTestRunner(verbosity=2).run(suite)

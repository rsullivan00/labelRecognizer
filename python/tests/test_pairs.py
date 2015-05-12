import unittest
from post_process import make_pairs, match_bipartite


class PairsTest(unittest.TestCase):
    make_pairs_tests = (
        ('Calories 1', [('Calories', '1', 0)]),
        ('Sad#um 81', [('Sad#um', '81', 0)])
    )

    def test_make_pairs(self):
        for in_str, test_tup in self.make_pairs_tests:
            result = make_pairs(in_str)
            self.assertEqual(test_tup, result)

    match_bipartite_tests = (
        (
            ([('calories', '1', 1), ('calaroes', '2', 2)], ['Calories']),
            [('Calories', '1', 1)]
        ),
    )

    def test_match_bipartite(self):
        for test_params, known_result in self.match_bipartite_tests:
            result = match_bipartite(test_params[0], test_params[1])
            self.assertEqual(known_result, result)


if __name__ == '__main__':
    unittest.main()

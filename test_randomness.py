#!/usr/bin/env python3
from collections import Counter
from pprint import pprint

from secret_santa import draw


GROUPS = [
    [(1, 1), (2, 2)],
    [(3, 3), (4, 4)],
    [(5, 5), (6, 6)],
]


def main():
    test_randomness()


def test_randomness():
    """ Repeat experiment to make sure it's fair """

    counter = Counter()

    for _ in range(100000):
        picks = draw(GROUPS)
        for (name, email), (target, _) in picks:
            counter[name, target] += 1

    pprint(counter)


if __name__ == '__main__':
    main()

# unit tests for likelihood functions
# some unit tests generated with ChatGPT.
import pytest
from .likelihood import invert_dictionary, initial_mapping, \
    update_mapping


def test_invert_dictionary():
    test_cases = [
        ({}, {}),
        ({'a': 1, 'b': 2, 'c': 3}, {1: 'a', 2: 'b', 3: 'c'}),
        ({'a': 1, 'b': 2, 'c': 1}, {1: 'c', 2: 'b'}),
        ({'apple': 'red', 'banana': 'yellow', 'grape': 'purple'},
         {'red': 'apple', 'yellow': 'banana', 'purple': 'grape'}),
        ({1: 'one', 2: 'two', 3: 'three'}, {'one': 1, 'two': 2, 'three': 3})
    ]

    for input_dict, expected_output in test_cases:
        assert invert_dictionary(input_dict) == expected_output


def test_update_mapping():
    with pytest.raises(TypeError):
        update_mapping(1712)
    d = initial_mapping()

    for _ in range(1000):
        dprime = update_mapping(d)
        diffs = 0
        assert d.keys() == dprime.keys()
        for key in d:
            if d[key] != dprime[key]:
                diffs += 1
        # should see two differences because two elements got swapped
        assert diffs == 2
        d = dprime

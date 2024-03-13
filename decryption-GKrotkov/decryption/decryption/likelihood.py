# helper functions to implement the Metropolis algorithm
import random
import math


def invert_dictionary(d):
    """Function to invert a python dictionary"""
    return dict((value, key) for key, value in d.items())


def initial_mapping():
    """Construct the null mapping"""
    return {"a": "a", "b": "b", "c": "c", "d": "d", "e": "e", "f": "f",
            "g": "g", "h": "h", "i": "i", "j": "j", "k": "k", "l": "l",
            "m": "m", "n": "n", "o": "o", "p": "p", "q": "q", "r": "r",
            "s": "s", "t": "t", "u": "u", "v": "v", "w": "w", "x": "x",
            "y": "y", "z": "z"}


def update_mapping(d):
    '''Updates the current mapping by randomly swapping two characters in the
    currently mapping.

    Sampling is without replacement. Function is nondestructive.

    Inputs
    ------
    d: dictionary representing the current mapping'''
    if not isinstance(d, dict):
        raise TypeError
    dprime = d.copy()
    key1, key2 = random.sample(list(dprime), 2)
    dprime[key1], dprime[key2] = dprime[key2], dprime[key1]
    return dprime


def pct_disagreement(d1, d2):
    """Counts the number of disagreements between two mappings

    Inputs
    ------
    d1, d2: decryption mappings, must have the same exact keys
    """
    disagreements = 0
    assert (d1.keys() == d2.keys())
    for key in d1:
        if d1[key] != d2[key]:
            disagreements += 1
    return disagreements / len(d1)


def likelihood_exponent(d, freqs, text):
    '''Computes the likelihood exponent of a given mapping based on a
    reference text.

    Inputs
    ------
    d: dictionary representing the mapping we want to compute the likelihood of
    frequencies: dictionary of counts of character pair observations in the
    reference text
    text: encrypted text

    Output
    ------
    '''
    likelihood = 0

    for i in range(1, len(text)):
        # retrieve each decoded mapping and create the character pair
        charpair = d.get(text[i - 1], " ") + d.get(text[i], " ")
        # we use the frequency log because it is more stable
        freq = freqs.get(charpair, 0)
        # if the pair does not appear, simply move on (do not take log(0))
        if freq > 0:
            # take sum instead of log because we're log-stabilizing the calc
            likelihood += math.log(freq)
    return likelihood


def likelihood_exp_diff(d, dprime, freqs, text):
    """Computes the likelihood difference of two decryption mappings

    Inputs
    ------
    d: current baseline mapping
    dprime: candidate new mapping
    freqs: reference text observed frequencies
    text: encrypted text
    p: tuning parameter"""
    d_exp = likelihood_exponent(d, freqs, text)
    dprime_exp = likelihood_exponent(dprime, freqs, text)
    return dprime_exp - d_exp


def likelihood_ratio(d, dprime, freqs, text):
    """
    Function to compute the likelihood ratio between two mappings.
    This function appears to be correct, but is too computationally intensive
    for use with entire texts.

    Inputs
    ------
    d: current baseline mapping
    dprime: candidate new mapping
    freqs: reference text observed frequencies
    text: encrypted text"""
    diff = likelihood_exp_diff(d, dprime, freqs, text)
    # the LR is the exp of the diff, using exponent rules
    ratio = math.exp(diff)
    return ratio

# functions to manage text
import re
import pickle
from .likelihood import initial_mapping, update_mapping


def preprocess_text(text, alphabet):
    """Function to preprocesses text

    Turns newlines into spaces, makes all text lowercase, removes all text not
    in the lowercase alphabet (and spaces), and then condenses spaces"""
    text = text.replace("\n", " ")
    text = text.lower()
    regex_remove = "[^" + alphabet + "]"
    text = re.sub(regex_remove, "", text)
    text = " ".join(text.split())
    if len(text) <= 1:
        raise ValueError
    return text


def read_text(filename, alphabet):
    """Function to read text given a filename, also preprocesses the text
    by removing non-space whitespace, repeat spaces, and punctuation."""
    reference = open(filename, 'r')
    text = reference.read()
    reference.close()
    return preprocess_text(text, alphabet)


def compute_frequencies(filename, alphabet, tofile="frequencies.pickle"):
    """Computes the frequencies of character pairs in a reference text

    Input
    ------
    filename - path to file to encrypt
    alphabet - characters to consider in the alphabet for this problem
    tofile - target pickle file"""
    text = read_text(filename, alphabet)
    d = dict()

    # start from 1 instead of 0 so we avoid indexOutOfBounds
    for i in range(1, len(text)):
        charpair = text[i - 1] + text[i]
        d[charpair] = d.get(charpair, 0) + 1

    # save the computed dictionary to a file
    # Pickle the list
    file = open(tofile, "wb")
    pickle.dump(d, file)
    file.close()


def encrypt_text(filename, alphabet, tofile="encrypted.pickle"):
    """Given a filename encrypts the given text using a random mapping.

    Inputs
    ------
    filename - path to file to encrypt
    alphabet - characters to consider in the alphabet for this problem
    tofile - target pickle file"""
    text = read_text(filename, alphabet)

    # construct the encryptor
    e = initial_mapping()
    for _ in range(1000):
        e = update_mapping(e)

    # apply the encryptor to the text
    new_text = ""
    for char in text:
        # if the char is not in e, it is a space so default to space
        new_text = new_text + e.get(char, " ")

    file = open(tofile, "wb")
    pickle.dump((new_text, e), file)
    file.close()


def decrypt_text(text, d, tofile="decrypted.txt"):
    """Function to decrypt text given a decryption key

    Inputs
    ------
    text - string input of text to decrypt
    d - decryption key (dictionary)
    tofile - target file for decryption"""
    decrypted = ""
    for char in text:
        decrypted = decrypted + d.get(char, " ")
    if tofile is not None:
        with open(tofile, 'w') as f:
            f.write(decrypted)
    return decrypted

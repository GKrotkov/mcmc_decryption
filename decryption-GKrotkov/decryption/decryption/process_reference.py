# code to preprocess the reference text
import string
import re
import pickle
import argparse


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


parser = argparse.ArgumentParser()
parser.add_argument("filename", action="store")
parser.add_argument("-d", "--debug", action="store_true")
args = parser.parse_args()

# Read the characters in the reference text
filename = args.filename
reference = open(filename, 'r')
text = reference.read()
reference.close()

alphabet = string.ascii_lowercase + " "
# Clean the text to have only alphabetic characters and spaces
text = preprocess_text(text, alphabet)

d = dict()

# start from 1 instead of 0 so we avoid indexOutOfBounds
for i in range(1, len(text)):
    charpair = text[i - 1] + text[i]
    d[charpair] = d.get(charpair, 0) + 1

# save the computed dictionary to a file
# Pickle the list
file = open("frequencies.pickle", "wb")
pickle.dump((d, alphabet), file)
file.close()

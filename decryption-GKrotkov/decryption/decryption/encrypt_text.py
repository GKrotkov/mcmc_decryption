# script to encrypt an input text
import string
import argparse
import pickle
from likelihood import initial_mapping, update_mapping
from process_reference import preprocess_text

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
text = preprocess_text(text, alphabet)

# construct the encryptor
e = initial_mapping()
for _ in range(1000):
    e = update_mapping(e)

# apply the encryptor to the text
new_text = ""
for char in text:
    # if the char is not in e, it is a space so default to space
    new_text = new_text + e.get(char, " ")


file = open("encrypted.pickle", "wb")
pickle.dump((new_text, e), file)
file.close()

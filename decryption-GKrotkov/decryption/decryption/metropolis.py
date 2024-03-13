import pickle
import string
import numpy as np
import argparse
from likelihood import initial_mapping, update_mapping, invert_dictionary, \
    likelihood_exponent, likelihood_exp_diff, pct_disagreement
from manage_text import read_text, compute_frequencies, \
    encrypt_text, decrypt_text

parser = argparse.ArgumentParser()
parser.add_argument("ref_filename", action="store")
parser.add_argument("encrypted_filename", action="store")
parser.add_argument("p", action="store")
parser.add_argument("-e", "--encrypt", action="store_true", default=False)
parser.add_argument("-d", "--debug", action="store_true", default=False)
args = parser.parse_args()

alphabet = string.ascii_lowercase + " "

# compute and unpack the reference frequencies
compute_frequencies(args.ref_filename, alphabet)
file = open("frequencies.pickle", "rb")
freqs = pickle.load(file)
file.close()

if args.encrypt:
    encrypt_text(args.encrypted_filename, alphabet)
    # load the encrypted text
    file = open("encrypted.pickle", "rb")
    encrypted, encryptor = pickle.load(file)
    file.close()
    d_true = invert_dictionary(encryptor)
else:
    encrypted = read_text(args.encrypted_filename, alphabet)

# setup
trials, early_stop, p = 10000, 1500, float(args.p)
mark = 0
d = initial_mapping()
best_mapping = d.copy()
best_score = likelihood_exponent(d, freqs, encrypted)

for i in range(trials):
    dprime = update_mapping(d)
    dprime_score = likelihood_exponent(dprime, freqs, encrypted)
    if (args.debug):
        print("i:", i, "candidate_score:", dprime_score,
              "current score:", likelihood_exponent(d, freqs, encrypted),
              "best score:", best_score)
    if dprime_score > best_score:
        if args.debug:
            print("found improvement!")
        mark = i
        # copy to break the aliasing (deepcopy not needed)
        best_mapping, best_score = dprime.copy(), dprime_score
    unif = np.random.uniform(0, 1)
    # Stablize the computation by taking log instead of exp
    # Uses exponent rules to only need to look at different of exps
    diff = likelihood_exp_diff(d, dprime, freqs, encrypted)
    threshold = np.log((unif ** (1 / p)))
    if threshold < diff:
        if args.debug:
            print("updating d!")
        d = dprime
    # early stopping condition
    if i > mark + early_stop:
        break

# if we know the true encryption, compare
# otherwise, output the decrypted text
if (args.encrypt):
    disagree = pct_disagreement(best_mapping, d_true)
    print("The best decryptor found with p =", p,
          "disagrees with the true decryptor", disagree,
          "percent of the time.")
else:
    print(best_mapping)
    decrypt_text(encrypted, best_mapping, "decrypted.txt")

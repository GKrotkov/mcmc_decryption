# __init__.py
from .likelihood import invert_dictionary, initial_mapping, update_mapping, \
    pct_disagreement, likelihood_exponent, likelihood_exp_diff, \
    likelihood_ratio

from .manage_text import preprocess_text, read_text, compute_frequencies, \
    encrypt_text, decrypt_text

from .test_likelihood import test_invert_dictionary, \
    test_update_mapping

# purely to avoid flake8 errors
invert_dictionary, initial_mapping, update_mapping, pct_disagreement
likelihood_exponent, likelihood_exp_diff, likelihood_ratio
preprocess_text, read_text, compute_frequencies, encrypt_text, decrypt_text
test_invert_dictionary, test_update_mapping

"""This module configures that alphabet."""


def _load_alphabet(filename):
    """
    Load a file containing the characters of the alphabet.
    Every unique character contained in this file will be used as a symbol
    in the alphabet.
    """
    with open(filename, 'r') as f:
        return list(set(f.read()))

def createalphabet(filename=None):
    """
    Creates a sample alphabet containing printable ASCII characters
    """
    if filename:
        return _load_alphabet(filename)

    alpha = []
    for i in range(58, 64):
        alpha.append(str(unichr(i)))
    for i in range(32, 57):
        alpha.append(str(unichr(i)))
    for i in range(65, 126):
        alpha.append(str(unichr(i)))
    return alpha

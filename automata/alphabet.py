"""This module configures that alphabet."""


def createalphabet():
    """
    Creates a sample alphabet containing printable ASCII characters
    """
    alpha = []
    for i in range(58, 64):
        alpha.append(str(unichr(i)))
    for i in range(32, 57):
        alpha.append(str(unichr(i)))
    for i in range(65, 126):
        alpha.append(str(unichr(i)))
    return alpha

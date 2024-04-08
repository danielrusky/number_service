import string
import random


def generate_string(length, symbols=None):
    if symbols is None:
        symbols = string.ascii_lowercase + string.digits
    return "".join(
        random.choice(symbols)
        for i in range(length)
    )



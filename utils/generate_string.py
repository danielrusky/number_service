import string
import random


def generate_string(length):
    return "".join(
        random.choice(string.ascii_lowercase + string.digits)
        for i in range(length)
    )



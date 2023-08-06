import random

from random_quote_generator.quotes import quotes


def get_quote() -> dict:

    """
    Get random quote

    Get a randomly selected quote from a database of quotes

    :return: selected quotes
    :rtype: dict
    """

    return quotes[random.randint(0, len(quotes) - 1)]

import random

from random_quote_generator.quotes import quotes


def get_quote() -> dict:

    """
    Get random quote

    Get randomly selected quote from database of famous quotes

    :return: selected quotes
    :rtype: dict
    """

    return quotes[random.randint(0, len(quotes) - 1)]

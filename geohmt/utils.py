


def random_string(string_length=3,seed = False):
    """Generates a random string of fixed length.

    Args:
        string_length (int, optional): Fixed length. Defaults to 3.
        seed (bool, optional): Weather uses seed. Defaults to False.

    Returns:
        _type_: A random string
    """    
    
    import random
    import string

    if seed:
        random.seed(1)

    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))
def clean_string(string: str) -> str:
    """
    Remove spaces and non-alpha numeric characters from string and makes all characters lowercase
    :param string: Dirty string
    :return: cleaned string
    """
    return ''.join(c for c in string if c.isalnum()).lower()

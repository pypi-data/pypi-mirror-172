"""provide a function that deterministically converts a dict to hash"""
import hashlib


def hash_dict(_dict):
    """sort, convert dict object to a URI-like string, hash it using SHA1"""
    string_list = []
    for tup in sorted(_dict.items()):
        string_list.append('='.join(str(tup)))

    return hashlib.sha1('&'.join(string_list).encode('utf-8')).hexdigest()

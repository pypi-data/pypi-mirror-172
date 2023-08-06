import hashlib


def uri_and_hash_from_dict(params, remove_keys: list = []):
    """Returns both uri and hash for a given dict, ignoring specific keys"""
    local_dict = subset_dict(params, remove_keys=remove_keys)
    uri = uri_string_from_dict(local_dict)
    query_hash = hash_from_uri_string(uri)
    return (uri, query_hash)


def hash_from_uri_string(uri_string:str):
    """Hashes a string for use with SERP components in the ecosystem"""
    hasher = hashlib.sha1()
    hasher.update(uri_string.encode('utf-8'))
    return hasher.hexdigest()


def uri_string_from_dict(input):
    """Create a uri string from a dictionary"""
    keys = list(input.keys())
    keys.sort()
    pre_hash = [f"{k}={input[k]}" for k in keys]
    return '&'.join(pre_hash)


def subset_dict(input, remove_keys: list = []):
    output = input.copy()
    [output.pop(k) for k in remove_keys]
    return output

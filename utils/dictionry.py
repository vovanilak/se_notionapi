
def insert_value(dictionary, value):
    if not isinstance(dictionary, dict):
        return

    keys = list(dictionary.keys())
    last_key = keys[-1]
    
    if isinstance(dictionary[last_key], dict):
        dictionary[last_key] = insert_value(dictionary[last_key], value)
    elif isinstance(dictionary[last_key], list):
        for i, item in enumerate(dictionary[last_key]):
            if isinstance(item, dict):
                dictionary[last_key][i] = insert_value(item, value)
    else:
        dictionary[last_key] = value
    
    return dictionary
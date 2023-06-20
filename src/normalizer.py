import json


def normalize_json(data, kwargs=None):
    if kwargs is not None:
        data = {**data, **kwargs}
    flattened = flatten_json(data)
    sorted = sort_json(flattened)
    result = json_to_value_string(sorted)
    return result


def flatten_json(data):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(data)
    return out


def sort_json(data):
    return json.loads(json.dumps(data, sort_keys=True, default=str))


def json_to_value_string(data):
    text_values = []
    for i in data.values():
        if isinstance(i, bool):
            t = 'true' if i else 'false'
        elif i is None:
            t = '#'
        elif isinstance(i, str) and i.strip() == '':
            t = '#'
        elif isinstance(i, list):
            t = ""
        elif isinstance(i, str):
            t = i.replace('#', "##")
        else:
            t = str(i)
        text_values.append(t)
    return '#'.join(text_values)

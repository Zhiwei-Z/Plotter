def create_name(keys, values):
    return ", ".join(["{}={}".format(str(k), str(v)) for k, v in zip(keys, values)])


def create_key_name(config, keys):
    values = [config[k] for k in keys]
    return create_name(keys, values)
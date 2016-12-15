import pytoml


def parse(_file):
    with open(_file) as conf_file:
        data = pytoml.loads(conf_file.read())

    return data

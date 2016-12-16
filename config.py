import pytoml


def parse(file):
    with open(file) as conf_file:
        data = pytoml.loads(conf_file.read())

    return data

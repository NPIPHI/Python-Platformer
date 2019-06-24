from mapElements import *


def load(map_name):
    file = open(map_name, 'r')
    text = file.read().splitlines()
    return list(map(eval, text))
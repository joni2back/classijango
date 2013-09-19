import re

def ucwords(string):
    return " ".join([w[0].upper() + w[1:] for w in re.split('\s*', string)])

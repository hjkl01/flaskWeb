import os
from config import logger


def search(path: str, word: str, _from: int = 1, _to: int = 1):
    logger.debug('%s %s %s %s' % (path, word, _from, _to))
    logger.debug(int(_from))
    dirs = os.listdir('%s%s' % ('/report/', path))
    temp = []
    for d in dirs:
        if word in d:
            temp.append(d)

    result = {}
    result['lengths'] = len(temp)
    result['result'] = temp[int(_from) - 1:int(_to)]
    return result

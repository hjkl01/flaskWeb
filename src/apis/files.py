import os
from config import logger


def files(d: dict = {}):
    try:
        _from = int(d.get('from')) - 1
        _to = int(d.get('to'))
        logger.info('%s %s' % (_from, _to))
    except Exception as err:
        return err

    path = d.get('path')
    full_list = [os.path.join(path, i) for i in os.listdir(path)]
    time_sorted_list = sorted(full_list, key=os.path.getmtime, reverse=False)
    sorted_filename_list = [os.path.basename(i) for i in time_sorted_list]
    logger.info(sorted_filename_list)
    # logger.info(type(sorted_filename_list))

    if _from < _to and _to - 1 < len(sorted_filename_list):
        files = sorted_filename_list[_from:_to]
    else:
        files = sorted_filename_list[_from:]

    result = {'lengths': len(sorted_filename_list), 'files': files}
    return result

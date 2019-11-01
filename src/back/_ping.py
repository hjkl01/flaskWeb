#!/usr/bin/env python3

import re
import multiprocessing, subprocess
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def run(ip, _dict):
    num = subprocess.call('ping -c 1 -W 1 %s' % ip, stdout=subprocess.PIPE, shell=True)
    if num == 0:
        logger.info('{} {}', ip, num)
        _dict[ip] = num
    else:
        logger.error('{} {}', ip, num)
        _dict[ip] = 1
    # return ip, num


def get_status(ip1, ip2=255):
    result = re.findall('(\d+)\.(\d+).(\d+).(\d+)', ip1)
    logger.info(result)

    temp_ip = '%s.%s.%s.' %(result[0][0], result[0][1], result[0][2])
    logger.info(temp_ip)

    ip_start = int(re.findall('.*\.(\d+)', ip1)[-1])
    ip_end = int(re.findall('.*\.(\d+)', ip2)[-1])

    manager = multiprocessing.Manager()
    _dict = manager.dict()
    jobs = []
    for i in range(ip_start, ip_end):
        ip = '%s%s' %(temp_ip, i)
        p = multiprocessing.Process(target=run, args=(ip, _dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    logger.info(dict(_dict))
    # logger.info(type(dict(_dict)))
    return dict(_dict)


if __name__ == '__main__':
    ip = '88.16.153.125'
    # ip = '192.168.2.6'
    get_status(ip)

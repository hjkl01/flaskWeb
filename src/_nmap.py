#!/usr/bin/env python3

import os
import re
import time
from multiprocessing import Process

from loguru import logger
logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def _nmap(ip, port):
    result = os.popen('nmap %s -p %s' % (ip, port))
    result = result.readlines()
    for i in range(len(result)):
        logger.info('%s:%s' % (i, result[i]))
    logger.info(result)
    if len(result) > 6:
        temp = result[6]
    else:
        return False
    logger.info(temp)
    if 'open' in temp:
        return True
    elif 'closed' in temp:
        return False
    else:
        return 'error'


def _ping(ip):
    out = os.popen('ping -c 3 %s' % ip).read()
    logger.info(out)
    temp = re.findall('(\d+)\%', out)
    logger.info(temp)
    if len(temp) >0 and temp[0] == '0':
        result = True
    else:
        result = False
    return result

def get_result(c):
    logger.info(c)
    s = re.compile('(\S+)\\t?(\d+\.\d+\.\d+\.\d+)\\t(\S+)')
    temp = re.findall(s, c)
    logger.info(temp)
    # [('VS_PK_new_txqd_yancheng_8866', '32.4.211.9', '8866')]
    if temp == []:
        logger.info('c is :%s' % c)
    else:
        temp = list(temp[-1])
        logger.info(temp)
        _dict = {}
        _dict['name'] = temp[0]
        _dict['ip'] = temp[1]
        _dict['port'] = temp[2]
        _dict['ping'] = _ping(temp[1])
        if temp[-1] == '0' or temp[-1] == 'any':
            logger.info('need not run _namp %s' % temp)
        else:
            _dict['nmap'] = _nmap(temp[1], temp[2])

    with open('ping_nmap_result.txt', 'a') as file:
        import json
        # file.write(json.dumps(result, ensure_ascii=False, indent=4))
        file.write('%s\n' % str(_dict))
        


def run():
    with open('ip_port.txt', 'r') as file:
        con = file.readlines()
    for c in con:
        p = Process(target=get_result, args=(c,))
        p.start()
        # p.join()
        time.sleep(0.5)
        # get_result(c)
        # break


if __name__ == '__main__':
    # ip = '127.0.0.1'
    # port = '23'
    # print(_nmap(ip, port))
    run()

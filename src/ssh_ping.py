#!/usr/bin/python

import paramiko
import re
import multiprocessing
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def ssh2(ip, port, username, passwd, target_ip, result_dict):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, username, passwd, timeout=5)
        cmd = 'ping -c 3 %s' % target_ip

        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.readlines()
        if len(out) == 8 and 'Unreachable' not in str(out):
            result_dict[target_ip] = 'exist'
        else:
            result_dict[target_ip] = 'error'

        logger.info('%s:\n%s' %(target_ip, out))
        ssh.close()
        # return out
    except:
        print('%s\tError\n' %(ip))


def run(_dict):
    result = re.findall('(\d+)\.(\d+).(\d+).(\d+)', _dict.get('target_ip1'))[0]
    logger.info(result)

    temp_ip = '%s.%s.%s.' %(result[0], result[1], result[2])
    logger.info(temp_ip)

    ip_start = int(re.findall('.*\.(\d+)', _dict.get('target_ip1'))[-1])
    ip_end = int(re.findall('.*\.(\d+)', _dict.get('target_ip2'))[-1])

    manager = multiprocessing.Manager()
    result_dict = manager.dict()
    jobs = []
    for i in range(ip_start, ip_end):
        cmd = ['ping -c 3 %s%s' %(temp_ip, i)]
        logger.info(cmd)
        p = multiprocessing.Process(
            target=ssh2,
            args=(
                _dict.get('server_ip'),
                _dict.get('server_port'),
                _dict.get('server_name'),
                _dict.get('server_passwd'),
                '%s%s' % (temp_ip, i),
                result_dict,
            ))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    logger.info(dict(result_dict))
    # logger.info(type(dict(_dict)))
    return dict(result_dict)


if __name__ == '__main__':
    _dict = {
        'server_ip': '88.16.153.3',
        'server_port': '22',
        'server_name': 'ljl',
        'server_passwd': '1',
        'target_ip1': '88.16.153.1',
        'target_ip2': '88.16.153.10',
    }
    run(_dict)

    # cmd = ['ping -c 3 -W 1 baidu.com', 'ping -c 3 google.com']
    # username = "ljl"
    # passwd = "1"

    # print("Begin......")
    # ip = '88.16.153.3'
    # port = 22
    # ssh2(ip, port, username, passwd, '88.16.153.3')

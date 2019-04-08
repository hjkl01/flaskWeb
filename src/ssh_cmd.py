#!/usr/bin/python

import paramiko
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def ssh_cmd(_dict):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        _dict.get('ip'),
        _dict.get('port'),
        _dict.get('username'),
        _dict.get('password'),
        timeout=5,
        allow_agent=False,
        look_for_keys=False)
    logger.info(_dict)
    stdin, stdout, stderr = ssh.exec_command('%s\n' % _dict.get('cmd'))
    out = '\n'.join(stdout.readlines())
    logger.info(out)
    ssh.close()
    result = {"result": out}
    return result


if __name__ == '__main__':
    _dict = {
        'ip': '66.10.254.2',
        'port': '22',
        'username': 'jsnx',
        'password': 'jmycisco',
        # 'cmd': 'display current-configuration'
        'cmd': 'display clock'
    }
    ssh_cmd(_dict)

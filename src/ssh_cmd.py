#!/usr/bin/python

import paramiko
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def ssh_cmd(_dict):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(_dict.get('ip'), _dict.get('port'), _dict.get('username'), _dict.get('password'), timeout=5)
        stdin, stdout, stderr = ssh.exec_command(_dict.get('cmd'))
        out = stdout.readlines()
        logger.info(out)
        ssh.close()
        result = {"result": out}
        return result
    except Exception as err:
        logger.error(err)
        return err


if __name__ == '__main__':
    _dict = {'ip': 'viewer.pub', 'port': '1080', 'username': 'ljl', 'password': 'jinlong', 'cmd': 'ls'}
    ssh_cmd(_dict)

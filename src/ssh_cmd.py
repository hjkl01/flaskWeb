#!/usr/bin/python

import paramiko
import netmiko
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def ssh_cmd(_dict):
    if str(_dict.get('factory_id')) == '4':
        return connect_huawei(_dict)
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
    # ssh.exec_command('terminal length 0 \n')
    stdin, stdout, stderr = ssh.exec_command('%s\n' % _dict.get('cmd'))
    out = '\n'.join(stdout.readlines())
    logger.info(out)
    ssh.close()
    result = {"result": out}
    return result


def connect_huawei(_dict):
    connection = netmiko.ConnectHandler(ip=_dict.get('ip'),
                                        device_type='huawei',
                                        username=_dict.get('username'),
                                        password=_dict.get('password'))
    logger.info(_dict)
    result = connection.find_prompt()
    result += connection.send_command('%s\n' % _dict.get('cmd'))
    logger.info(result)
    logger.info(type(result))
    connection.disconnect()
    return {'result': str(result)}


if __name__ == '__main__':
    _dict = {
        'ip': '66.10.254.2',
        'port': '22',
        'username': 'jsnx',
        'password': 'jmycisco',
        'factory_id': 4,
        # 'cmd': 'display current-configuration'
        # 'cmd': 'display clock'
        'cmd': 'display cpu'
    }
    ssh_cmd(_dict)

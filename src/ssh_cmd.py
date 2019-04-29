#!/usr/bin/python

import paramiko
from netmiko import Netmiko
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'),
           format="{time:MM-DD HH:mm:ss} {level} {message}")


def ssh_cmd(_dict):
    logger.info(_dict.get('factory_id'))
    if _dict.get('factory_id'):
        factory_ids = {
            "4": "huawei",
            "8": "cisco_nxos",
            "12": "juniper",
            "16": None,
        }
        new_dict = {
            'ip': _dict.get('ip'),
            'port': _dict.get('port'),
            'username': _dict.get('username'),
            'password': _dict.get('password'),
            'device_type': factory_ids.get(str(_dict.get('factory_id')))
        }
        logger.info(new_dict)
        return use_netmiko(new_dict, _dict.get('cmd'))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        _dict.get('ip'),
        port=_dict.get('port'),
        username=_dict.get('username'),
        password=_dict.get('password'),
        timeout=5,
        allow_agent=False,
        look_for_keys=False)
    logger.info(_dict)
    # ssh.exec_command('terminal length 0 \n')
    # ssh.exec_command('set length 0\n')
    stdin, stdout, stderr = ssh.exec_command('%s\n' % _dict.get('cmd'))
    out = stdout.read()
    logger.info(out)
    ssh.close()
    result = {"result": out}
    return result


def use_netmiko(_dict, cmd):
    net_connect = Netmiko(**_dict)

    # send_command_timing as the router prompt is not returned
    output = net_connect.send_command_timing(
        cmd, strip_command=False, strip_prompt=False)
    i = 0
    temp = net_connect.send_command_timing(
        " \n", strip_command=False, strip_prompt=False)
    while 'more' in temp:
        temp = net_connect.send_command_timing(
            " \n", strip_command=False, strip_prompt=False)
        # print(temp)
        output += temp
        i += 1
        logger.info(i)

    net_connect.disconnect()
    # logger.info(output)
    return {"result":output}


if __name__ == '__main__':
    _dict = {
        'ip': '32.3.242.1',
        'port': '22',
        'username': 'jsnx',
        'password': 'jmycisco',
        # 'device_type': 'juniper',
        'factory_id': 12,
        # 'cmd': 'display current-configuration'
        # 'cmd': 'display clock'
        'cmd': 'get system'
        }
    ssh_cmd(_dict)

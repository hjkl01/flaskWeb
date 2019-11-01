#!/usr/bin/python

from pydantic import BaseModel
import paramiko
from netmiko import Netmiko
from config import logger


class Cmd(BaseModel):
    factory_id: str = None
    ip: str
    port: str
    username: str
    password: str
    cmd: str


async def ssh_cmd(_dict: Cmd):
    logger.info(_dict.factory_id)
    if _dict.factory_id:
        factory_ids = {
            "4": "huawei",
            "8": "cisco_ios",
            "12": "juniper",
            "16": None,
        }
        new_dict = {
            'ip': _dict.ip,
            'port': _dict.port,
            'username': _dict.username,
            'password': _dict.password,
            'device_type': factory_ids.get(str(_dict.factory_id))
        }
        logger.info(new_dict)
        return use_netmiko(new_dict, _dict.cmd)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(_dict.ip,
                port=_dict.port,
                username=_dict.username,
                password=_dict.password,
                timeout=5,
                allow_agent=False,
                look_for_keys=False)
    logger.info(_dict)
    # ssh.exec_command('terminal length 0 \n')
    # ssh.exec_command('set length 0\n')
    stdin, stdout, stderr = ssh.exec_command('%s\n' % _dict.cmd)
    out = stdout.read()
    logger.info(out)
    ssh.close()
    result = {"result": out}
    return result


def use_netmiko(_dict, cmd):
    net_connect = Netmiko(**_dict)

    # send_command_timing as the router prompt is not returned
    output = net_connect.send_command_timing(cmd,
                                             strip_command=False,
                                             strip_prompt=False)
    i = 0
    temp = net_connect.send_command_timing(" \n",
                                           strip_command=False,
                                           strip_prompt=False)
    while 'more' in temp or 'More' in temp:
        temp = net_connect.send_command_timing(" \n",
                                               strip_command=False,
                                               strip_prompt=False)
        logger.info(temp)
        output += temp
        i += 1
        logger.info(i)

    net_connect.disconnect()
    logger.info(output)
    return {'result': output}


if __name__ == '__main__':
    _dict = {
        'ip': '66.5.11.219',
        'port': '22',
        'username': 'admin',
        'password': 'admin',
        # 'device_type': 'cisco_ios',
        'factory_id': 8,
        # 'cmd': 'display current-configuration'
        # 'cmd': 'display clock'
        'cmd': 'show run'
    }
    ssh_cmd(_dict)

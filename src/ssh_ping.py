#!/usr/bin/python

import threading
import paramiko
import multiprocessing
import os
import re
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class Ssh_ping:
    def __init__(self, _dict):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(_dict.get('server_ip'), _dict.get('server_port'), _dict.get('server_name'), _dict.get('server_passwd'), timeout=5)
        logger.info('connect success %s' % self.ssh)

    def ssh2(self, target_ip):
        try:
            cmd = 'ping -c 3 %s' % target_ip
            logger.debug(cmd)

            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            out = stdout.readlines()
            logger.debug(out)
            if len(out) == 8 and 'Unreachable' not in str(out):
                result = True
            else:
                result = False

            logger.info('%s:\n%s' % (target_ip, out))
            return result
        except Exception as err:
            result = False
            logger.error('%s %s' % (err, target_ip))
            return result

    def close(self):
        self.ssh.close()


def parse_dict(_dict):
    result = re.findall('(\d+)\.(\d+).(\d+).(\d+)', _dict.get('target_ip1'))[0]
    # logger.info(result)

    start_ip = '%s.%s.%s.' % (result[0], result[1], result[2])
    logger.info(start_ip)

    ip_from = int(re.findall('.*\.(\d+)', _dict.get('target_ip1'))[-1])
    ip_to = int(re.findall('.*\.(\d+)', _dict.get('target_ip2'))[-1]) + 1
    return start_ip, ip_from, ip_to


def _ping(ip):
    cmd = 'ping -c 3 %s' % ip
    logger.info(cmd)
    out = os.popen(cmd).readlines()
    if len(out) == 8 and 'Unreachable' not in str(out):
        result = True
    else:
        result = False
    return ip, result


def ssh_ping(_dict):
    # def _ping(cmds): return os.popen(cmds[-1]).readlines()
    start_ip, ip_from, ip_to = parse_dict(_dict)
    if 'server_ip' not in _dict.keys():
        result = {}

        pool = multiprocessing.Pool(processes=4)
        temp_results = []
        for i in range(ip_from, ip_to):
            ip = '%s%s' % (start_ip, i)
            # logger.info(ip)
            temp_results.append(pool.apply_async(_ping, (ip, )))
        pool.close()
        pool.join()
        logger.info("Sub-process(es) done.")
        # logger.info([r.get() for r in temp_results])

        result = {}
        for res in temp_results:
            # logger.info(res.get())
            result[res.get()[0]] = res.get()[1]

    else:
        ob = Ssh_ping(_dict)
        result = {}
        for i in range(ip_from, ip_to):
            target_ip = '%s%s' % (start_ip, i)
            temp = ob.ssh2(target_ip)
            result[target_ip] = temp
        ob.close()
    logger.info(result)
    return result


if __name__ == '__main__':
    _dict = {
        'server_ip': '66.3.47.31',
        'server_port': '22',
        'server_name': 'dc',
        'server_passwd': '2019',
        'target_ip1': '66.3.47.30',
        'target_ip2': '66.3.47.35',
    }
    _dict = {
        'target_ip1': '88.16.153.23',
        'target_ip2': '88.16.153.35',
    }
    ssh_ping(_dict)
    # curl -i -H "Content-Type: application/json" -X POST -d '{"target_ip1":"66.3.47.30", "target_ip2":"66.3.47.35"}' http://127.0.0.1:8001/ping
    # curl -i -H "Content-Type: application/json" -X POST -d '{"server_ip":"66.3.47.31", "server_port":"22","server_name":"dc","server_passwd":"2019", "target_ip1":"66.3.47.30", "target_ip2":"66.3.47.35"}' http://127.0.0.1:8001/ping

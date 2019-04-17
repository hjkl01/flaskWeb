#!/usr/bin/env python3

# import telnetlib1 as telnetlib
import telnetlib
import time
from loguru import logger
logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def telnet_cmd(_dict):
    ip = _dict.get('ip').encode()
    username = _dict.get('username').encode()
    password = _dict.get('password').encode()

    tn = telnetlib.Telnet(ip, port=23, timeout=50)
    # tn.set_debuglevel(2)
    logger.info("loginning...")
    tn.read_until(b"Username:")
    tn.write(username + b"\n")
    tn.write(password + b"\n")
    time.sleep(1)

    tn.write(b"%s\r\n" % _dict.get('cmd').encode())

    # for i in range(100):
    #     tn.write(b" \r\n")
    #     logger.info(i)
    # temp = tn.read_eager()
    # if b"Config" in temp:
    #     logger.info(temp)
    #     break

    time.sleep(5)
    logger.info(_dict.get('cmd'))
    tn.read_until(b'>')

    result = tn.read_very_eager()
    logger.info('read_very_eager %s' % result)

    result = tn.read_lazy()
    logger. info('all', result)
    tn.close()


def test(_dict):
    from telneter import Account, Executor
    a = Account(_dict.get('username'), _dict.get('password'))
    ex = Executor(_dict.get('ip'), account=a)
    print(ex.cmd('get conf'))


if __name__ == '__main__':
    _dict = {
        'ip': '66.16.254.254',
        'port': '23',
        'username': 'cisco',
        'password': 'cisco',
        'cmd': 'show version'
    }
    # telnetip(_dict)
    _dict = {
        'ip': '66.5.253.5',
        'port': '23',
        'username': 'jsnx',
        'password': 'jmycisco',
        'cmd': 'get conf'
    }
    test(_dict)
    # telnetip(_dict)

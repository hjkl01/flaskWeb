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
    time.sleep(3)
    # tn.read_until(b"login")
    tn.write(username + b"\n")
    time.sleep(1)
    tn.write(password + b"\n")
    time.sleep(1)

    tn.write(b"%s\r\n" % _dict.get('cmd').encode())

    time.sleep(3)
    logger.info(_dict.get('cmd'))
    time.sleep(5)

    result = b''
    i = 0
    while 1:
        i += 1
        # tn.read_until(b'more')
        temp = tn.read_very_eager()
        logger.info(temp)
        result += temp
        # logger.info(temp)
        # if b'more' in temp or b'More' in temp:
        if b'more' in temp.lower(): 
            # logger.info('input \\n')
            tn.write(b' \n')
            time.sleep(1)
        else:
            print(temp)
            break
        logger.info(i)
    # tn.read_until(b'>')
    tn.close()

    logger.info('read_very_eager %s' % result)
    return {'result': result}


if __name__ == '__main__':
    _dict = {
        # 'ip': '32.3.224.21',
        # 'ip': "66.5.254.130",
        'ip': '66.10.254.254',
        'port': '23',
        'username': 'jsnx',
        # 'password': '04nuaa07',
        'password': 'jmycisco',
        # 'cmd': 'show run'
        'cmd': 'display cur'
    }
    telnet_cmd(_dict)

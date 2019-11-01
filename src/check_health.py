import time
import json
from multiprocessing import Process

import pymysql
import requests
from loguru import logger

from config import config

logger.add("logs/%s.log" % __file__.rstrip('.py'),
           format="{time:MM-DD HH:mm:ss} {level} {message}",
           retention="30 days",
           level='INFO')


def req(cnf):
    try:
        conn = pymysql.connect(host=cnf.get('host'),
                               user=cnf.get('user'),
                               passwd=cnf.get('passwd'),
                               db=cnf.get('db'))
        cur = conn.cursor()
        cur.execute("SELECT VERSION()")
        for r in cur:
            print(r)
        cur.close()
        conn.close()
        return 200
    except Exception as err:
        return err


def send_msg(_id=0, status=2, msg=None):
    url = config.msg_url
    if status == 1:
        _id = str(time.time()).replace('.', '')
    logger.info(f"send msg .... {_id} {status}")
    # debug
    # return _id
    data = {
        "SourceEventID":
            f"{_id}",
        "SourceCIName":
            "MySQL server down",
        "SourceAlertKey":
            "MYSQL",
        "SourceSeverity":
            "2",
        "SourceIdentifier":
            "",
        "LastOccurrence":
            f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}',
        "Summary":
            msg,
        "SourceID":
            3,
        "Severity":
            1,
        "Status":
            status
    }
    logger.debug(data)
    rep = requests.post(url, data=json.dumps(data))
    logger.debug(rep.status_code)
    logger.info(rep.text)
    return _id


def run(cnf):
    status = 1
    global _id
    _id = 0
    while True:
        logger.debug(f'{_id} {status}')
        status_code = req(cnf)
        if status_code == 200:
            logger.info('服务正常 %s' % status_code)
            if status == 0:
                msg = f"Mysql{cnf.get('host')} 服务恢复正常"
                try:
                    send_msg(_id, status=2, msg=msg)
                except Exception as err:
                    logger.error(err)
                status = 1
        else:
            logger.error('服务出错！%s' % status_code)
            if status == 1:
                status = 0
                msg = f"Mysql{cnf.get('host')} 服务异常 ！"
                try:
                    _id = send_msg(status=1, msg=msg)
                except Exception as err:
                    logger.error(err)
        time.sleep(1)


def main():
    logger.debug(config.check_health_mysql_01)
    cnfs = [config.check_health_mysql_01, config.check_health_mysql_02]
    for cnf in cnfs:
        p = Process(target=run, args=(cnf, ))
        p.start()
    # run(config.check_health_mysql_01)


if __name__ == "__main__":
    # run()
    # send_msg()
    main()

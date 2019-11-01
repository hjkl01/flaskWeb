#!/usr/bin/env python3

import time
import os
import json
from config import config
import mysql.connector
from loguru import logger
logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")

"""
CREATE TABLE alarm_keyword_db
(
`id` int NOT NULL AUTO_INCREMENT,
`keyword` varchar(255) NOT NULL,
`level` int NOT NULL,
`content` varchar(255),
`insert_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`status` int NOT NULL DEFAULT 1,
PRIMARY KEY (id)
)
"""


class Cron:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=config.mysql_host,
            user=config.mysql_user,
            passwd=config.mysql_pass,
            database='nxcloud')
        logger.info(self.mydb)

    def _select(self, sql):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult

    def _insert(self, sql):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql)
        self.mydb.commit()
        logger.info('success \n%s' % sql)

    def cron(self):
        sql = "select keyword,level from alarm_keyword_db where status=1"
        temp = self._select(sql)
        logger.info(temp)
        for t in temp:
            today = time.strftime("%Y.%m.%d", time.localtime())
            url = 'http://66.3.47.31:9200/index-%s/_search?q=%s' % (today, t[0])
            var = os.popen('curl %s' % url).read()
            temp_result = self.parse(var)
            if len(temp_result) < 1:
                continue
            for r in temp_result:
                logger.info(r)
                sql = 'insert into alarm_record_tb (alarm_time,alarm_key, content, device_info, level) values ("{0}", "elk", "{1}", "{2}", "{3}")'.format(r.get('_time'), r.get('message'), r.get('host'), t[1])
                self._insert(sql)
        return

    def parse(self, _str):
        temp = json.loads(_str)
        var = temp.get('hits').get('hits')
        result = []
        for v in var:
            temp_dict = {}
            _dict = v.get('_source')
            temp_dict['_time'] = _dict.get('@timestamp')
            temp_dict['message'] = _dict.get('message')
            temp_dict['host'] = _dict.get('host')
            result.append(temp_dict)
        logger.info(result)
        return result


if __name__ == '__main__':
    run = Cron()
    # run.parse()
    run.cron()

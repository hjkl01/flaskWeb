#!/usr/bin/env python3

from config import logger
import config
import mysql.connector
from pydantic import BaseModel
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


class Message(BaseModel):
    # message = "{'port': 34918, 'tags': ['_grokparsefailure'], '@version': '1', '@timestamp': '2019-05-05T07:56:06.907Z', 'host': 'gateway', 'type': 'syslog', 'message': '<173>Oct  7 13:57:16 2011 PK_YPT_GXY_Core-SW %%10SHELL/5/SHELL_LOGIN: jsnx logged in from 66.3.47.31.\\u0000'}"
    message: dict = {}


class Alarm:

    def __init__(self, message):
        self.mydb = mysql.connector.connect(host=config.mysql_host,
                                            user=config.mysql_user,
                                            passwd=config.mysql_pass,
                                            database='nxcloud')
        self.message_json = eval(message)
        logger.debug(self.message_json)
        logger.debug(self.mydb)

    def _select(self, sql):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult

    def _insert(self, sql):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql)
        self.mydb.commit()
        logger.debug('success \n%s' % sql)

    def alarm(self):
        sql = "select keyword,level from alarm_keyword_db where status=1"
        temp = self._select(sql)
        logger.debug(temp)
        for t in temp:
            logger.debug(self.message_json)
            logger.debug(t)
            if t[0] in self.message_json.get('message'):
                logger.debug(t)
                sql = 'insert into alarm_record_tb (alarm_time,alarm_key, content, device_debug, level) values ("{0}", "elk", "{1}", "{2}", "{3}")'.format(
                    self.message_json.get('@timestamp'), self.message_json.get('message'),
                    self.message_json.get('host'), t[1])
                self._insert(sql)
                break
        return


async def run(message: Message):
    go = Alarm(message.message)
    go.alarm()
    return 'success'


if __name__ == '__main__':
    message = "{'port': 34918, 'tags': ['_grokparsefailure'], '@version': '1', '@timestamp': '2019-05-05T07:56:06.907Z', 'host': 'gateway', 'type': 'syslog', 'message': '<173>Oct  7 13:57:16 2011 PK_YPT_GXY_Core-SW %%10SHELL/5/SHELL_LOGIN: jsnx logged in from 66.3.47.31.\\u0000'}"
    run = Alarm(message)
    run.alarm()

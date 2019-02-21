#!/usr/bin/env python3

import time
import mysql.connector
from ssh_cmd import ssh_cmd
from loguru import logger
logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")

mydb = mysql.connector.connect(host="66.3.47.33", user="root", passwd="root", database='nxcloud')
logger.info(mydb)


def _select(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


def _insert(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    logger.info('success \n%s' % sql)


def run():
    sql = "select %s from %s" % ('device_id, command, command_id', 'device_config_command_tb')
    commands = _select(sql)
    logger.info(commands)
    for command in commands:
        sql = 'select ip_adress, user_name, device_password from device_tb where device_id = %s' % command[0]
        # logger.info(sql)
        devices_info = _select(sql)
        # logger.info(devices_info)
        for device in devices_info:
            logger.info(device)
            _dict = {'ip': device[0], 'port': '22', 'username': device[1], 'password': device[2], 'cmd': command[1]}

            try:
                tmp_result = ssh_cmd(_dict)
                logger.info(tmp_result)
                sql = 'insert into device_config_tb (device_id,command_id,config_content,config_version) values ("{0}", "{1}", "{2}", "{3}")'.format(
                    command[0], command[2], tmp_result.get('result').decode('utf8').replace('\r','').replace('\n',''), str(time.ctime()))
                logger.info(sql)
                _insert(sql)
            except Exception as err:
                logger.error(err)


if __name__ == '__main__':
    run()
    # sql = 'select config_content from device_config_tb'
    # logger.info(_select(sql))

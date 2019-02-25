#!/usr/bin/env python3

import time
import yaml
import mysql.connector
from ssh_cmd import ssh_cmd
from loguru import logger
logger.add(
    "logs/%s.log" % __file__.rstrip('.py'),
    format="{time:MM-DD HH:mm:ss} {level} {message}")


class Cron:
    def __init__(self):
        with open('settings.yaml', 'r') as file:
            self.config = yaml.load(file)
        self.mydb = mysql.connector.connect(
            host=self.config.get('mysql_host'),
            user=self.config.get('mysql_user'),
            passwd=self.config.get('mysql_pass'),
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
        sql = "select %s from %s" % ('device_id, command, command_id',
                                     'device_config_command_tb')
        commands = self._select(sql)
        logger.info(commands)
        for command in commands:
            sql = 'select ip_adress, user_name, device_password from device_tb where device_id = %s' % command[
                0]
            # logger.info(sql)
            devices_info = self._select(sql)
            # logger.info(devices_info)
            for device in devices_info:
                logger.info(device)
                _dict = {
                    'ip': device[0],
                    'port': '22',
                    'username': device[1],
                    'password': device[2],
                    'cmd': command[1]
                }

                try:
                    tmp_result = ssh_cmd(_dict)
                    logger.info(tmp_result)
                    sql = 'insert into device_config_tb (device_id,command_id,config_content,config_version) values ("{0}", "{1}", "{2}", "{3}")'.format(
                        command[0], command[2],
                        tmp_result.get('result').decode('utf8').replace(
                            '\r', '').replace('\n', ''), str(time.ctime()))
                    logger.info(sql)
                    self._insert(sql)
                except Exception as err:
                    logger.error(err)

    def devices_test_cmd(self, _dict):
        result = {}
        for device_id in _dict.get('deviceIds').split(','):
            sql = 'select ip_adress, user_name, device_password from device_tb where device_id = %s' % device_id
            device = self._select(sql)[-1]
            logger.info(device)
            cmd_dict = {
                'ip': device[0],
                'port': '22',
                'username': device[1],
                'password': device[2],
                'cmd': _dict.get('command')
            }
            tmp_result = ssh_cmd(cmd_dict)
            result[device_id] = tmp_result.get('result').decode(
                'utf8').replace('\r', '').replace('\n', '')
        logger.info(result)
        return result


if __name__ == '__main__':
    # cron()
    # sql = 'select config_content from device_config_tb'
    # logger.info(_select(sql))
    _dict = {'deviceIds': '3,13', 'command': "show version"}
    run = Cron()
    run.devices_test_cmd(_dict)

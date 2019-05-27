#!/usr/bin/env python3

import time
import config
import mysql.connector
from ssh_cmd import ssh_cmd
from telnet_cmd import telnet_cmd
from loguru import logger
logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


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

    def cron(self, command_id=None):
        if command_id == 'all':
            sql = "select %s from %s" % ('device_id, command, command_id', 'device_config_command_tb')
        elif command_id == None:
            return
        else:
            sql = "select %s from %s where command_id=%s" % ('device_id, command, command_id', 'device_config_command_tb', command_id)

        commands = self._select(sql)
        logger.info(commands)
        result = []
        for command in commands:
            _temp_dict = {
                'device_id': command[0],
                'command': command[1],
                'command_id': command[2],
                'error': ''
            }
            sql = 'select ip_adress, user_name, device_password, factory_id,login_function from device_tb where device_id = %s' % command[0]
            # logger.info(sql)
            device = self._select(sql)[-1]
            # logger.info(devices_info)
            logger.info(device)
            _dict = {
                'ip': device[0],
                'port': '22',
                'username': device[1],
                'password': device[2],
                'cmd': command[1],
                'factory_id': device[3]
            }

            if str(device[4]) == '3':
                tmp_result = telnet_cmd(_dict)
            else:
                tmp_result = ssh_cmd(_dict)
            try:
                logger.info(tmp_result)
                # java 端会提前判断command是否可执行，省略判断
                try:
                    sql = 'insert into device_config_tb (device_id,command_id,config_content,config_version) values ("{0}", "{1}", "{2}", "{3}")'.format(command[0], command[2], tmp_result.get('result').decode('utf8').replace('"', '\\"'), str(time.ctime()))
                except:
                    sql = 'insert into device_config_tb (device_id,command_id,config_content,config_version) values ("{0}", "{1}", "{2}", "{3}")'.format(command[0], command[2], tmp_result.get('result').replace('"', '\\"'), str(time.ctime()))
                # logger.info(sql)
                self._insert(sql)
            except Exception as err:
                _temp_dict['error'] = err
                logger.error(err)
            result.append(_temp_dict)
        rresult = {}
        rresult['result'] = result
        return rresult

    def devices_test_cmd(self, _dict):
        result = {}
        for device_id in _dict.get('deviceIds').split(','):
            sql = 'select ip_adress, user_name,device_password,factory_id,login_function from device_tb where device_id = %s' % device_id
            device = self._select(sql)[-1]
            logger.info(device)
            cmd_dict = {
                'ip': device[0],
                'port': '22',
                'username': device[1],
                'password': device[2],
                'factory_id': device[3],
                'cmd': _dict.get('command')
            }
            if str(device[4]) == '3':
                tmp_result = telnet_cmd(cmd_dict)
            else:
                tmp_result = ssh_cmd(cmd_dict)
            try:
                result[device_id] = tmp_result.get('result').decode('utf8').replace('"', '\\"')
            except:
                result[device_id] = tmp_result.get('result').replace('"', '\\"')
        # logger.info(result)
        return result


if __name__ == '__main__':
    # cron()
    # sql = 'select config_content from device_config_tb'
    # logger.info(_select(sql))
    logger.info(Cron().cron(20))
    # _dict = {'deviceIds': '3,13', 'command': "show versio"}
    # run = Cron()
    # run.devices_test_cmd(_dict)

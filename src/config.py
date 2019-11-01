from loguru import logger
logger.add("logs/%s.log" % __file__.rstrip('.py'),
           format="{time:MM-DD HH:mm:ss} {level} {message}")

mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_pass = 'root'

zabbix = '127.0.0.1.8081'

elk = '127.0.0.1:9200'

# grafana_host = '88.16.153.36'
grafana = '127.0.0.1:8000'

msg_url = 'http://66.6.51.64:10016/http/rest/noma'

# check_health_mysql_01:
#     host: 32.12.129.18
#     user: root
#     passwd: root
#     db: root
#
# check_health_mysql_02:
#     host: 32.12.65.19
#     user: root
#     passwd: root
#     db: root

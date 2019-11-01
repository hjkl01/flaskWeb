from config import logger
import config
import grequests


async def send_request():
    be_urls = {}
    be_urls['zabbix'] = f'http://{config.zabbix}'
    be_urls['elk'] = f'http://{config.elk}'
    be_urls['grafana'] = f'http://{config.grafana}'
    logger.debug(be_urls)
    # {'zabbix': '127.0.0.1.8081', 'elk': '127.0.0.1.9200', 'grafana': '127.0.0.1.8000'}

    urls = [v for k, v in be_urls.items()]
    rs = (grequests.get(u) for u in urls)
    temp = [True if r is not None else False for r in grequests.map(rs)]
    result = {}
    result['zabbix'] = temp[0]
    result['elk'] = temp[1]
    result['grafana'] = temp[2]
    logger.debug(result)
    return result


if __name__ == '__main__':
    send_request()

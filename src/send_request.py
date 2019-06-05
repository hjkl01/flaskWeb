from loguru import logger
import multiprocessing
from config import config
import requests

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def crawler(url, server_name):
    try:
        rep = requests.get(url, timeout=3)
        print(rep.status_code)
        return server_name, rep.status_code
    except Exception as err:
        return server_name, err


def run():
    result = {}
    result['zabbix'] = {'host': config.zabbix_host, 'port': config.zabbix_port}
    result['elk'] = {'host': config.elk_host, 'port': config.elk_port}
    result['grafana'] = {'host': config.grafana_host, 'port': config.grafana_port}
    logger.info(result)
    # {'zabbix': {'host': '66.3.47.31', 'port': 8081}, 'elk': {'host': '66.3.47.31', 'port': 80}, 'grafana': {'host': '66.3.47.31', 'port': 8000}}

    pool = multiprocessing.Pool(processes=3)
    temp_results = []
    for server_name, h_p in result.items():
        # print(h_p)
        host = h_p.get('host')
        port = h_p.get('port')
        url = 'http://%s:%s' % (host, port)
        logger.debug(url)
        temp_results.append(pool.apply_async(crawler, (url, server_name, )))
    pool.close()
    pool.join()
    logger.info("Sub-process(es) done.")

    result = {}
    for res in temp_results:
        # logger.debug(res.get())
        if res.get()[0] == 200:
            result[res.get()[0]] = True
        else:
            logger.info(res.get()[1])
            result[res.get()[0]] = False

    logger.info(result)
    return result


if __name__ == '__main__':
    run()

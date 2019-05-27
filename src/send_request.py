from loguru import logger
import multiprocessing
import yaml
import requests

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def crawler(url, server_name):
    try:
        rep = requests.get(url)
        print(rep.status_code)
        return server_name, rep.status_code
    except Exception as err:
        return server_name, err


def run():
    with open('settings.yaml', 'r') as file:
        config = yaml.load(file)
    result = {}
    result['zabbix'] = {'host': config.get('zabbix_host'), 'port': config.get('zabbix_port')}
    result['elk'] = {'host': config.get('elk_host'), 'port': config.get('elk_port')}
    result['grafana'] = {'host': config.get('grafana_host'), 'port': config.get('grafana_port')}
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
        # logger.info(res.get())
        if res.get()[1] == 200:
            result[res.get()[0]] = True
        else:
            logger.info(res.get()[1])
            result[res.get()[0]] = False

    logger.info(result)
    return result


if __name__ == '__main__':
    run()

import nmap
import yaml
import multiprocessing
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


def python_nmap(host, port, server_name):
    nm = nmap.PortScanner()
    nm.scan(host, str(port))
    # print(nm.command_line())
    # logger.info(nm.scaninfo())

    # logger.info('state', nm['127.0.0.1'].state())  # (up|down|unknown|skipped)
    logger.info(nm[host]['tcp'])
    result = nm[host]['tcp'].get(int(port))['state']
    logger.info(result)
    return server_name, result


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
        print(h_p)
        host = h_p.get('host')
        port = h_p.get('port')
        temp_results.append(pool.apply_async(python_nmap, (host, port, server_name, )))
    pool.close()
    pool.join()
    logger.info("Sub-process(es) done.")

    result = {}
    for res in temp_results:
        # logger.info(res.get())
        if res.get()[1] == 'closed':
            result[res.get()[0]] = 0
        elif res.get()[1] == 'open':
            result[res.get()[0]] = 1
        else:
            result[res.get()[0]] = 'error'

    logger.info(result)
    return result


if __name__ == '__main__':
    host = '127.0.0.1'
    port = '22'
    # python_nmap(host, port)
    run()

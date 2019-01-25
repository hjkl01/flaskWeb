#!/usr/bin/env python

from ssh_ping import run
from flask import Flask, jsonify, redirect, request
app = Flask(__name__)

from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


@app.route('/')
def index():
    # _str = '''参数例子: ./ip/88.16.153.125/88.16.153.135\n'''
    _str = ''' curl -i -H "Content-Type: application/json" -X POST -d '{"server_ip":"88.16.153.3","server_port":"22","server_name":"username","server_passwd":"password","target_ip1":"88.16.153.1","target_ip2":"88.16.153.10"}' http://127.0.0.1:8000/json'''
    return _str


@app.route('/json', methods=['POST'])
# @app.route('/json', methods=['GET', 'POST'])
def _ip():
    logger.info(request.method)
    logger.info(request.json)
    return jsonify(run(request.json))


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8000)

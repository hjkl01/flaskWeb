#!/usr/bin/env python

import subprocess
import os
from ssh_ping import run
from flask import Flask, jsonify, redirect, request
from werkzeug import secure_filename
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


def run_commands(cmd):
    my_env = os.environ.copy()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, env=my_env)
    output, error = process.communicate()
    return output


@app.route('/ansible/example')
def _ansible_example():
    cmd = "ansible-playbook -i hosts task.yml"
    output = run_commands(cmd)
    logger.info(output)
    return output


@app.route('/ansible', methods=['GET', 'POST'])
def _ansible():
    if request.method == 'POST':
        file = request.files['hosts']
        hosts = secure_filename(file.filename)
        file.save(os.path.join('%s/config' % os.getcwd(), hosts))
        file = request.files['yml']
        yml = secure_filename(file.filename)
        file.save(os.path.join('%s/config' % os.getcwd(), yml))
        logger.info('upload success %s %s' % (hosts, yml))
        cmd = 'ansible-playbook -i config/%s config/%s' % (hosts, yml)
        result = run_commands(cmd)
        logger.info(result)
        return result
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=hosts>
             <input type=file name=yml>
             <input type=submit value=Upload>
          </p>
        </form>
        '''


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8000)

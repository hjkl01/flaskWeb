#!/usr/bin/env python

import subprocess
import os
from ssh_ping import ssh_ping
from ssh_cmd import ssh_cmd
# from cron_device_conf import cron, devices_test_cmd
from cron_device_conf import Cron
from ansible_api import ansible_api
from flask import Flask, jsonify, redirect, request, render_template
from werkzeug import secure_filename
from concurrent.futures import ThreadPoolExecutor

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(2)
app = Flask(__name__)

from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ping', methods=['POST'])
def ping_ip():
    logger.info(request.method)
    logger.info(request.json)
    return jsonify(ssh_ping(request.json))


@app.route('/cmd', methods=['POST'])
def run_cmd():
    logger.info(request.method)
    logger.info(request.json)
    return jsonify(ssh_cmd(request.json))


@app.route('/device', methods=['POST'])
def _device():
    logger.info(request.method)
    logger.info(request.json)
    return jsonify(Cron().devices_test_cmd(request.json))


@app.route('/cron/<command_id>', methods=['GET', 'POST'])
def _cron(command_id):
    logger.info(request.method)
    return jsonify(Cron().cron(command_id))


@app.route('/crons', methods=['GET', 'POST'])
def _crons():
    logger.info(request.method)
    executor.submit(Cron().cron('all'))
    return 'task cron was runned in background'


def run_commands(cmd):
    my_env = os.environ.copy()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, env=my_env)
    output, error = process.communicate()
    return output


# @app.route('/ansible/example')
# def _ansible_example():
#     cmd = "ansible-playbook -i hosts task.yml"
#     output = run_commands(cmd)
#     logger.info(output)
#     return output


@app.route('/ansible_cmd/<filename>', methods=['GET', 'POST'])
def _ansible_cmd(filename):
    cmd = 'ansible-playbook -i tasks/%s tasks/%s.yml' % (filename, filename)
    result = run_commands(cmd)
    return result


#@app.route('/test/<filename>', methods=['GET', 'POST'])
@app.route('/ansible/<filename>')
def _ansible(filename):
    hosts_path = 'tasks/%s' % filename
    yml_path = 'tasks/%s.yml' % filename
    logger.info('host path : %s, yml path : %s' % (hosts_path, yml_path))
    result = ansible_api(hosts_path, yml_path)
    logger.info(result)
    return jsonify(result)


# @app.route('/ansible', methods=['GET', 'POST'])
# def _ansible():
#     if request.method == 'POST':
#         file = request.files['hosts']
#         hosts = secure_filename(file.filename)
#         file.save(os.path.join('%s/config' % os.getcwd(), hosts))
#         file = request.files['yml']
#         yml = secure_filename(file.filename)
#         file.save(os.path.join('%s/config' % os.getcwd(), yml))
#         logger.info('upload success %s %s' % (hosts, yml))
#         cmd = 'ansible-playbook -i config/%s config/%s' % (hosts, yml)
#         result = run_commands(cmd)
#         logger.info(result)
#         return result
#     else:
#         return render_template('upload.html')


@app.route('/files', methods=['GET', 'POST'])
def _files():
    logger.info(request.json)
    try:
        _from = int(request.json.get('from')) - 1
        _to = int(request.json.get('to'))
        logger.info('%s %s' % (_from, _to))
    except Exception as err:
        return err

    path = request.json.get('path')
    full_list = [os.path.join(path, i) for i in os.listdir(path)]
    time_sorted_list = sorted(full_list, key=os.path.getmtime, reverse=False)
    sorted_filename_list = [os.path.basename(i) for i in time_sorted_list]
    logger.info(sorted_filename_list)
    # logger.info(type(sorted_filename_list))

    if _from < _to and _to - 1 < len(sorted_filename_list):
        files = sorted_filename_list[_from:_to]
    else:
        files = sorted_filename_list[_from:]

    result = {'lengths': len(sorted_filename_list), 'files': files}
    return jsonify(result)


@app.route('/search/<path:path>/<path:word>/<path:_from>/<path:_to>')
def search(path, word, _from=1, _to=1):
    logger.info('%s %s %s %s' % (path, word, _from, _to))
    logger.info(int(_from))
    dirs = os.listdir('%s%s' % ('/report/', path))
    temp = []
    for d in dirs:
        if word in d:
            temp.append(d)

    result = {}
    result['lengths'] = len(temp)
    result['result'] = temp[int(_from) - 1:int(_to)]
    return jsonify(result)


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')
    return redirect('/')


@app.errorhandler(500)
def errer_500(e):
    return render_template('404.html')
    return redirect('/')


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8001)

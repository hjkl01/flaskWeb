import os
import subprocess
from config import logger
from apis.ansible_api import ansible_api
from pydantic import BaseModel


async def run_commands(cmd):
    my_env = os.environ.copy()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, env=my_env)
    output, error = process.communicate()


async def ansible_cmd(f: str):
    cmd = '/p2/bin/ansible-playbook -i tasks/%s tasks/%s.yml' % (f, f)
    result = run_commands(cmd)
    return result


async def ansible_filename(f: str):
    hosts_path = 'tasks/%s' % f
    yml_path = 'tasks/%s.yml' % f
    logger.debug('host path : %s, yml path : %s' % (hosts_path, yml_path))
    result = ansible_api(hosts_path, yml_path)
    logger.debug(result)
    return result

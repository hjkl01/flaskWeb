#!/usr/bin/env python3


import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.task_ok={}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()]=result


results_callback = ResultCallback()

#InventoryManager类
loader = DataLoader()     #读取yaml文件
inventory = InventoryManager(loader=loader, sources=['tasks/task'])#这里的路径要正确
#variableManager类
variable_manager = VariableManager(loader=loader,inventory=inventory)

#option 执行选项
Options = namedtuple('Optoins',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'syntax',
                      'listtags',
                      'listtasks',
                      'sudo_user',
                      'sudo',
                      'diff'])

options = Options(connection='smart',
                   remote_user=None,
                   ack_pass=None,
                   sudo_user=None,
                   forks=5,
                   sudo=None,
                   ask_sudo_pass=False,
                   verbosity=5,
                   module_path=None,
                   become=None,
                   become_method=None,
                   become_user=None,
                   check=False,
                   diff=False,
                   listhosts=None,
                   listtasks=None,
                   listtags=None,
                   syntax=None)


passwords=dict()

#playbook的路径要正确
playbook=PlaybookExecutor(playbooks=['tasks/task.yml'],
                          inventory=inventory,
                          variable_manager=variable_manager,
                          loader=loader,
                          options=options,
                          passwords=passwords)

#playbook.run()

playbook._tqm._stdout_callback=results_callback
playbook.run()

results_raw={'ok':{}}

for host,result in results_callback.task_ok.items():
    results_raw['ok'][host]=result._result

print(results_raw)

print(results_callback)

## /ping
```sh
    curl -i -H "Content-Type: application/json" -X POST -d '{"server_ip":"88.16.153.3","server_port":"22","server_name":"username","server_passwd":"password","target_ip1":"88.16.153.1","target_ip2":"88.16.153.10"}' http://127.0.0.1:8001/json
```

## /ansible

### 点击选择文件上传 

#### 第一个应为hosts

```sh

[cisco]
# 66.16.254.254
66.16.254.1 ansible_ssh_user=cisco ansible_ssh_pass=cisco ansible_ssh_port=22

[h3c]
# export ANSIBLE_HOST_KEY_CHECKING=False
66.5.254.130 ansible_ssh_user=jsnx ansible_ssh_pass=jmycisco ansible_ssh_port=22
66.10.254.1 ansible_ssh_user=jsnx ansible_ssh_pass=jmycisco ansible_ssh_port=22
```
#### 第二个为task.yml
```sh
---
- name: test route
  hosts: cisco
  gather_facts: false
  connection: local

  tasks:
    - name: test 
      ios_command:
        commands:
          - show version
            # - show interfaces

      register: output

    - debug: msg="Hello World! {{ output.stdout }}"

```

## /files

```sh
curl -i -H "Content-Type: application/json" -X POST -d '{"path":"config", "from":"1", "to":"5"}' http://127.0.0.1:8001/files
```

## /search/folder_name/file_name/from/to

> from 和to 需为数字

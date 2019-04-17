FROM ubuntu:latest
COPY sources.list /etc/apt/sources.list
RUN apt update -y
RUN apt install python3 python3-pip sshpass git vim iputils-ping -y
RUN apt install nmap -y
# RUN mkdir /sockets
COPY . /app
COPY vimrc /root/.vimrc
COPY config ~/.ssh/config
COPY ansible.cfg /etc/ansible/ansible.cfg
WORKDIR /app
RUN pip3 install -r /app/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# CMD /usr/local/bin/uwsgi --ini /app/uwsgi.ini
CMD python3 main.py

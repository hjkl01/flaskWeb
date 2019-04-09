FROM ubuntu:latest
COPY sources.list /etc/apt/sources.list
COPY ping /usr/local/bin/
RUN apt update -y
RUN apt install python3 python3-pip sshpass git -y
RUN mkdir /sockets
COPY . /app
COPY ansible.cfg /etc/ansible/ansible.cfg
WORKDIR /app
RUN pip3 install -r /app/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# CMD /usr/local/bin/uwsgi --ini /app/uwsgi.ini
CMD python3 main.py

FROM ubuntu:latest
COPY config/sources.list /etc/apt/sources.list
COPY config/pip /root/.pip

RUN apt update -y
RUN apt install python3 python3-pip sshpass git vim iputils-ping -y
RUN apt install python2.7 python-pip supervisor -y

RUN pip install virtualenv -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN virtualenv -p /usr/bin/python2 /p2
RUN /p2/bin/pip install ansible -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

# RUN mkdir /sockets
COPY . /app
COPY config/vimrc /root/.vimrc
COPY config/config ~/.ssh/config
COPY ansible.cfg /etc/ansible/ansible.cfg
WORKDIR /app
RUN pip3 install -r /app/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# RUN python3 /app/create_cron_task.py
# CMD /usr/local/bin/uwsgi --ini /app/uwsgi.ini
CMD python3 main.py
# CMD gunicorn -c gunicorn.py main:app

# COPY config/supervisor.conf /etc/supervisor/conf.d/
# CMD ["/usr/bin/supervisord","-n"]


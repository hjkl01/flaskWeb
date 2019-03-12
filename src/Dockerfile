FROM python:3.6.1
RUN pip install --upgrade pip -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN mkdir /sockets 
COPY . /app
COPY ansible.cfg /etc/ansible/ansible.cfg
WORKDIR /app
RUN pip install -r /app/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# CMD /usr/local/bin/uwsgi --ini /app/uwsgi.ini
CMD python main.py

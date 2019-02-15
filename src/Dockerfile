FROM python:3.6.1
RUN pip install --upgrade pip -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN pip install uwsgi -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN mkdir /sockets 
COPY uwsgi.ini /etc/uwsgi/
COPY . /app
WORKDIR /app
ADD requirements.txt /
RUN pip install -r /requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
CMD /usr/local/bin/uwsgi --ini /etc/uwsgi/uwsgi.ini
#--ini /app/uwsgi.ini

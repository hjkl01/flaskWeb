#!/usr/bin/env python3

# pip install python-crontab
from crontab import CronTab

my_cron = CronTab(user='root')
job = my_cron.new(command='python3 /app/cron_alarm.py')
job.minute.every(1)

my_cron.write()

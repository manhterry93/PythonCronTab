# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import logging

import crontab
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    logging.info(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.
    logging.info('dir: ' + dir_path)


def setup_cron_job():
    logging.info('setup cron job')
    temp_cron = crontab.CronTab(user='manhpv')
    py_file = dir_path + '/psu.py'
    job = temp_cron.new(command='python3 {}'.format(py_file), comment="psu_job")
    job.hour.every(1)
    temp_cron.write()


def disable_job():
    logging.info('disable job')
    temp_cron = crontab.CronTab(user='manhpv')
    for job in temp_cron:
        if job.comment == 'psu_job':
            logging.info(job)
            temp_cron.remove(job)
            temp_cron.write()


def check_job():
    logging.info('check job')
    my_crons = crontab.CronTab(user='manhpv')
    for job in my_crons:
        logging.info(job)
        logging.info(job.is_valid())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(filename='cron_job.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    print_hi('PyCharm')
    args = sys.argv
    # setup_cron_job()
    # disable_job()
    # check_job()
    globals()[args[1]](*args[2:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

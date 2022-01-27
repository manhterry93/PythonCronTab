# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import logging

import crontab
import sys
import os
import getpass

dir_path = os.path.dirname(os.path.realpath(__file__))


def setup_cron_job():
    logging.info('--------Setup cron job---------')
    temp_cron = crontab.CronTab(user=getpass.getuser())
    py_file = dir_path + '/psu.py'
    job = temp_cron.new(command='python3 {}'.format(py_file), comment="psu_job")
    job.hour.every(1)
    temp_cron.write()


def disable_job():
    logging.info('--------Disable job---------')
    temp_cron = crontab.CronTab(user=getpass.getuser())
    for job in temp_cron:
        if job.comment == 'psu_job':
            logging.info(job)
            temp_cron.remove(job)
            temp_cron.write()


def check_job():
    """
    Check job for username
    :return: Job exist or not (with comment="psu_job")
    """
    logging.info('---------Check job--------')
    my_crons = crontab.CronTab(user=getpass.getuser())
    exist = False
    for job in my_crons:
        if job.comment == 'psu_job':
            exist = True
        logging.info(job)
        logging.info('job valid: {}'.format(job.is_valid()))
    return exist


def remove_all():
    """
    remove all job with comment="psu_job"
    :return:
    """
    logging.info('------Remove all job---------')
    my_crons = crontab.CronTab(user=getpass.getuser())
    my_crons.remove_all(comment='psu_job')
    my_crons.write()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(filename='cron_job.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    args = sys.argv
    # setup_cron_job()
    # disable_job()
    # check_job()
    globals()[args[1]](*args[2:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

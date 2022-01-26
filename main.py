# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import crontab
import sys


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


def setup_cron_job():
    print('setup cron job')
    temp_cron = crontab.CronTab(user='manhpv')
    job = temp_cron.new(command='python3 /home/manhpv/BackendProjects/CronJob/write_date.py', comment="test_job")
    job.minute.every(1)
    temp_cron.write()
    print(job)


def disable_job():
    print('disable job')
    temp_cron = crontab.CronTab(user='manhpv')
    for job in temp_cron:
        if job.comment == 'test_job':
            print(job)
            temp_cron.remove(job)
            temp_cron.write()


def check_job():
    print('check job')
    my_crons = crontab.CronTab(user='manhpv')
    for job in my_crons:
        print(job)
        print(job.is_valid())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    args = sys.argv
    # setup_cron_job()
    # disable_job()
    # check_job()
    globals()[args[1]](*args[2:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

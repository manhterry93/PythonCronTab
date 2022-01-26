import psutil
import sys


def check_memory():
    print('virtual memory: {}'.format(psutil.virtual_memory()))
    print('swap memory: {}'.format(psutil.swap_memory()))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = sys.argv
    # setup_cron_job()
    # disable_job()
    # check_job()
    globals()[args[1]](*args[2:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

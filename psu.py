import psutil
import sys

RAM_THRESHOLD = 3221225472  # 3GB


def check_memory():
    print('virtual memory: {}'.format(psutil.virtual_memory().available))
    # Check available RAM in Bytes
    virtual_memory = psutil.virtual_memory().available
    if virtual_memory >= RAM_THRESHOLD:
        # Reset mongo db from here
        pass
    print('swap memory: {}'.format(psutil.swap_memory()))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = sys.argv
    # setup_cron_job()
    # disable_job()
    # check_job()
    globals()[args[1]](*args[2:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

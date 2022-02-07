import os

import psutil
import sys
import subprocess
import datetime
import pymongo
from pymongo import ReadPreference
import logging
import json

RAM_THRESHOLD = 1073741824   # 1GB
# RAM_THRESHOLD = 10737418240  # 10GB

dir_path = os.path.dirname(os.path.realpath(__file__))
config = {}


def check_process():
    """
    Check process to logging the mongodb status:
    * Total instance count
    * Total Memory consume
    """
    listOfProcObjects = []
    mongo_count = 0
    mongo_total_size = 0
    logging.info('------Logging mongo processes memory---')
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms
            # Append dict to list
            if pinfo['name'] == 'mongod':
                mongo_count += 1
                mongo_total_size += pinfo['vms']
                listOfProcObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        # Sort list of dict by key vms i.e. memory usage

    # listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)

    # with open('processes.txt', 'w') as outFile:
    #     # Iterate over all running processes
    #     for item in listOfProcObjects:
    #         outFile.write(json.dumps(item) + '\n')
    #     outFile.close()
    log_data = {
        "mongo_count": mongo_count,
        "mongo_total_size": mongo_total_size
    }
    logging.info("mongo processes detail: {}".format(log_data))
    check_mongo_status()


def check_memory():
    logging.info("\n--------Checking Memory---------")
    print('virtual memory: {}'.format(psutil.virtual_memory().available))
    # Check available RAM in Bytes
    virtual_memory = psutil.virtual_memory().available
    logging.info(
        "Available RAM: {} MB/{} MB".format(bytes_to_MB(virtual_memory), bytes_to_MB(psutil.virtual_memory().total)))
    if virtual_memory < RAM_THRESHOLD:
        logging.info("RAM below threshold ({} MB)".format(bytes_to_MB(RAM_THRESHOLD)))
        check_process()
    else:
        logging.info("No need to reset mongo docker\n")


def check_mongo_status():
    """
    Check status of mongo db, if current mongo is Primary in replicaset,
    reset mongo db docker
    """
    logging.info("Checking mongo status...")
    if not load_config():
        return
    try:
        client = pymongo.MongoClient(config['mongo_uri'])
        client_role = client.read_preference.name
        # if client_role.lower() == "primary":
        #     logging.info("Mongo client is PRIMARY  ==> Reset")
        client.close()
        reset_mongo_docker()
    except Exception as e:
        logging.info("Check mongo status failed with error")
        logging.error(e)


def reset_mongo_docker():
    try:
        logging.info("Resetting mongo docker...")
        # We will replace first param by result of command: whereis docker-compose
        subprocess.run(["/usr/local/bin/docker-compose", "-f",
                        config['docker-compose_file_path'], "restart",
                        config['service_name']])
    except Exception as e:
        logging.info("Error in reset mongo docker")
        logging.error(e)


def bytes_to_MB(bytes):
    return int(bytes / 1048576)


def load_config():
    logging.info("Loading config...")
    global config
    try:
        file = open("{}/config.json".format(dir_path), "r")
        config_str = file.read()
        config = json.loads(config_str)
        file.close()
        return True
    except Exception as e:
        logging.info("Error in loading config")
        logging.error(e)
        return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(filename='{}/psu.log'.format(dir_path), level=logging.DEBUG, format='%(asctime)s %(message)s')
    check_memory()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

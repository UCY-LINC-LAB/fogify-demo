from time import sleep

import requests
import os
def get_random_metrics(data_size=10, filesize=1000000, file="/data/yellow_tripdata_2018-01.csv"):
    import random
    data = []
    f = open(file, "r")

    offset = random.randrange(filesize)
    f.seek(offset)  # go to random position


    for i in range(0,data_size):
        f.readline()  # discard - bound to be partial line
        random_line = f.readline()
        data+=[random_line]

    f.close()
    return data

def propagate_to_edge(data):
    sent = False
    for region in ['bronx', 'brooklyn', 'manhattan', 'queens', 'satenisland']:
        try:
            requests.post("http://fogify_edge-node-%s.region_%s:8000/"%(region, region), data=str(data), timeout=10)
            sent=True
            break
        except:
            continue
    if not sent:
        try:
            requests.post("http://fogify_cloud-server.internet:8000/", data=str(data))
        except Exception as e:
            print(e)
            print("data is lost")
            # sleep(5)
            # propagate(data=data)


def propagate(data):
    try:
        requests.post("http://fogify_cloud-server.internet:8000/", data=str(data))
    except Exception as e:
        print(e)
        print("data is lost")
        sleep(5)
        propagate(data=data)

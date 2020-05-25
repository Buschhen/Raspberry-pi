import requests
from datetime import datetime
import os

# Get the time stamp for filename and to check time
# model it for crontab


def timestamp():
    # format to string
    timestamp = str(datetime.now())
    timestamp = timestamp.replace(' ', '').replace(':', '').replace('-', '')
    dot = timestamp.find(".") - 2
    # format time to cut of seconds
    unix = timestamp[0:dot]
    unix = int(unix)
    return unix


while True:
    unixtime = timestamp()
    if unixtime % 2 == 0:
        urls = open("URLS.txt", "r")
        for line in urls:
            url = line.strip()
            if not (os.path.isdir("./rawdata")):
                os.makedirs("./rawdata")
            if url.find("index") > 0:
                stonks = url[url.find("index") + 6:]
                if not (os.path.isdir(f"./rawdata/raw{stonks}")):
                    os.makedirs(f"./rawdata/raw{stonks}")

            elif url.find("aktien") > 0:
                stonks = url[url.find("aktien") + 7:url.find("-")]
                if not (os.path.isdir(f"./rawdata/raw{stonks}")):
                    os.makedirs(f"./rawdata/raw{stonks}")

            if not (os.path.isfile(f"./rawdata/raw{stonks}/{stonks}-{unixtime}.html")):
                site = str(requests.get(url).content).replace(
                    '\\t', '').replace('\\n', "").replace('\\r', '')
                rawdata = open(
                    f"./rawdata/raw{stonks}/{stonks}-{unixtime}.html", "a")
                rawdata.write(site)
                rawdata.close()
